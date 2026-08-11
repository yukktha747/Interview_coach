import os
from crewai.tools import tool
from crewai import LLM

from src.indexing.qdrant_store import search_with_rerank

# Shared LLM config — DeepSeek via OpenRouter (free tier)
# CrewAI uses LiteLLM under the hood, so the "openrouter/" prefix routes correctly.
def get_llm():
    return LLM(
        model="openrouter/deepseek/deepseek-chat",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


@tool("Search Interview Knowledge Base")
def search_knowledge_base(query: str) -> str:
    """
    Searches the interview question bank (RAG, vector DBs, LLM systems) and
    returns the most relevant question/answer/rubric chunks for a given query.
    Uses two-stage retrieval: dense search over a wider candidate pool,
    narrowed by a cross-encoder reranker for higher precision.
    Use this to find questions to ask, or to find the ground-truth rubric when
    evaluating a candidate's answer.
    """
    results = search_with_rerank(query, first_stage_k=8, final_k=3)
    if not results:
        return "No relevant content found."

    formatted = []
    for r in results:
        formatted.append(f"[score={r['score']:.3f}] {r['text']}")
    return "\n\n---\n\n".join(formatted)


if __name__ == "__main__":
    print(search_knowledge_base("What is reciprocal rank fusion?"))