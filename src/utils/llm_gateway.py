import time
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, List, Optional

import litellm
from dotenv import load_dotenv

from src.utils.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)


@dataclass
class GatewayCallResult:
    content: str
    model_used: str
    latency_ms: float
    cache_hit: bool
    cost_usd: float = 0.0


class LLMGateway:
    """
    A minimal LLM gateway: sits between your code and the LLM provider(s),
    adding three things a raw API call doesn't give you —

    1. Fallback: if the primary model fails (rate limit, timeout, provider
       outage), automatically retries against a backup model instead of
       just failing the whole request.
    2. Caching: identical (model, messages) requests within the TTL return
       a cached response instantly, at zero cost — useful for repeated
       eval runs or identical test prompts during development.
    3. Cost/latency tracking: every call is logged with how long it took
       and (roughly) what it cost, so you have visibility instead of a
       black box.

    This wraps litellm directly (not going through CrewAI), so it's usable
    standalone for e.g. your RAGAS judge calls or any place you make a raw
    LLM call outside the agent framework.
    """

    def __init__(self, models: list[str], cache_ttl_seconds: int = 300):
        """
        models: ordered list of litellm-style model strings, e.g.
                ["openrouter/deepseek/deepseek-chat", "openrouter/openai/gpt-4o-mini"]
                The first is primary; the rest are fallbacks tried in order
                if the previous one raises.
        """
        if not models:
            raise ValueError("LLMGateway needs at least one model")
        self.models = models
        self.cache_ttl = cache_ttl_seconds
        self._cache: dict[str, tuple[float, str]] = {}  # key -> (timestamp, content)

    def _cache_key(self, model: str, messages: list[dict]) -> str:
        raw = json.dumps({"model": model, "messages": messages}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _check_cache(self, key: str) -> str | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        timestamp, content = entry
        if time.time() - timestamp > self.cache_ttl:
            del self._cache[key]
            return None
        return content

    def call(self, messages: list[dict]) -> GatewayCallResult:
        primary_key = self._cache_key(self.models[0], messages)
        cached = self._check_cache(primary_key)
        if cached is not None:
            logger.info(f"Gateway cache HIT for primary model {self.models[0]}")
            return GatewayCallResult(
                content=cached, model_used=self.models[0],
                latency_ms=0.0, cache_hit=True,
            )

        last_exception = None
        for i, model in enumerate(self.models):
            start = time.time()
            try:
                response = litellm.completion(
                    model=model,
                    messages=messages,
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    base_url="https://openrouter.ai/api/v1" if model.startswith("openrouter/") else None,
                )
                latency_ms = (time.time() - start) * 1000
                content = response.choices[0].message.content

                try:
                    cost = litellm.completion_cost(completion_response=response)
                except Exception:
                    cost = 0.0

                if i > 0:
                    logger.warning(f"Gateway fell back to model #{i+1} ({model}) after prior failure")
                logger.info(
                    f"Gateway call: model={model} latency={latency_ms:.0f}ms "
                    f"cost=${cost:.6f}"
                )

                self._cache[self._cache_key(model, messages)] = (time.time(), content)

                return GatewayCallResult(
                    content=content, model_used=model,
                    latency_ms=latency_ms, cache_hit=False, cost_usd=cost,
                )

            except Exception as e:
                last_exception = e
                logger.warning(f"Gateway: model {model} failed ({e}), trying next fallback if any")
                continue

        logger.error(f"Gateway: all {len(self.models)} model(s) failed. Last error: {last_exception}")
        raise last_exception


# ---------------------------------------------------------------------------
# LangChain adapter — makes LLMGateway usable anywhere a LangChain chat model
# is expected (e.g. RAGAS's LangchainLLMWrapper).
#
# This is a REAL BaseChatModel subclass, not a hand-rolled lookalike. RAGAS
# calls fairly deep LangChain methods (agenerate_prompt, generate_prompt,
# etc.) that are implemented by LangChain's own base class on top of just
# _generate/_agenerate — subclassing properly gets all of that for free,
# instead of us having to guess which methods RAGAS needs and reimplement
# each one individually.
# ---------------------------------------------------------------------------
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from pydantic import ConfigDict


class GatewayChatModel(BaseChatModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    gateway: Any = None

    @property
    def _llm_type(self) -> str:
        return "llm-gateway"

    def _messages_to_dicts(self, messages: List[BaseMessage]) -> list[dict]:
        role_map = {"human": "user", "ai": "assistant", "system": "system"}
        return [
            {"role": role_map.get(m.type, m.type), "content": m.content}
            for m in messages
        ]

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        formatted = self._messages_to_dicts(messages)
        result = self.gateway.call(formatted)
        message = AIMessage(content=result.content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        # Gateway itself is sync-only for now — fine at this project's scale.
        # A true production gateway would use litellm's async completion here.
        return self._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


if __name__ == "__main__":
    gateway = LLMGateway(models=[
        "openrouter/deepseek/deepseek-chat",
        "openrouter/meta-llama/llama-3.1-8b-instruct:free",  # verify this slug is still valid on OpenRouter
    ])

    messages = [{"role": "user", "content": "In one sentence, what is reciprocal rank fusion?"}]

    result1 = gateway.call(messages)
    print(f"First call — model={result1.model_used}, cache_hit={result1.cache_hit}, "
          f"latency={result1.latency_ms:.0f}ms, cost=${result1.cost_usd:.6f}")
    print(result1.content)

    result2 = gateway.call(messages)
    print(f"\nSecond call (same input) — cache_hit={result2.cache_hit}")