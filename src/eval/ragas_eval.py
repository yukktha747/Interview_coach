import json
import os

from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness, ResponseRelevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

from src.utils.llm_gateway import LLMGateway, GatewayChatModel

load_dotenv()

# Routed through the LLM gateway instead of calling ChatOpenAI directly —
# gets automatic fallback to a backup model, response caching (useful since
# RAGAS re-evaluates the same session data on every dev iteration of this
# script), and cost/latency logging for free.
_gateway = LLMGateway(models=[
    "openrouter/deepseek/deepseek-chat",
    "openrouter/meta-llama/llama-3.1-8b-instruct:free",  # verify this slug is still valid on OpenRouter
])
judge_llm = LangchainLLMWrapper(GatewayChatModel(gateway=_gateway))

judge_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)


def load_session_log(path: str = "session_log.json") -> list[dict]:
    with open(path) as f:
        return json.load(f)


def build_ragas_dataset(session_log: list[dict]) -> EvaluationDataset:
    """
    Two samples per round: one for the Interviewer's question (grounded in /
    relevant to the retrieved topic context), one for the Evaluator's grading
    (grounded in the retrieved rubric).
    """
    samples = []
    for round_record in session_log:
        samples.append(
            SingleTurnSample(
                user_input=f"Ask an interview question about: {round_record['topic']}",
                retrieved_contexts=round_record["question_context"],
                response=round_record["question"],
            )
        )
        samples.append(
            SingleTurnSample(
                user_input=round_record["question"],
                retrieved_contexts=round_record["evaluation_context"],
                response=round_record["evaluation_reasoning"],
            )
        )
    return EvaluationDataset(samples=samples)


def run_evaluation(session_log_path: str = "session_log.json"):
    session_log = load_session_log(session_log_path)
    if not session_log:
        print("Session log is empty — run session_graph.py through at least one full round first.")
        return

    dataset = build_ragas_dataset(session_log)

    results = evaluate(
        dataset=dataset,
        metrics=[Faithfulness(), ResponseRelevancy()],
        llm=judge_llm,
        embeddings=judge_embeddings,
    )

    df = results.to_pandas()
    print(df)  # print everything — column names can vary by ragas version, safer than guessing

    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        print(f"Average {col}: {df[col].mean():.3f}")

    return results


if __name__ == "__main__":
    run_evaluation()