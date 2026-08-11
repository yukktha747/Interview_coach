import os
import requests
from dotenv import load_dotenv

from src.utils.retry import retry_with_backoff
from src.utils.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)

JINA_API_KEY = os.getenv("JINA_API_KEY")
JINA_RERANK_URL = "https://api.jina.ai/v1/rerank"
JINA_RERANK_MODEL = "jina-reranker-v2-base-multilingual"


@retry_with_backoff(max_attempts=3, exceptions=(requests.exceptions.RequestException,))
def rerank(query: str, documents: list[str], top_n: int = 3) -> list[dict]:
    """
    Cross-encoder reranking: jointly scores (query, document) pairs, which is
    more accurate than the bi-encoder cosine similarity used for first-stage
    retrieval, but too slow to run over a full corpus — hence the two-stage
    retrieve-then-rerank pattern.

    Returns a list of dicts sorted by relevance, each:
    {"text": ..., "score": ..., "original_index": ...}
    """
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY not found in environment")

    if not documents:
        return []

    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": JINA_RERANK_MODEL,
        "query": query,
        "documents": documents,
        "top_n": min(top_n, len(documents)),
        "return_documents": True,
    }

    logger.info(f"Reranking {len(documents)} candidate(s) for query: {query[:50]!r}")
    response = requests.post(JINA_RERANK_URL, headers=headers, json=payload)

    if response.status_code == 429:
        logger.warning("Jina rerank API rate limited (429)")
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data["results"]:
        doc = item["document"]
        doc_text = doc["text"] if isinstance(doc, dict) else doc
        results.append({
            "text": doc_text,
            "score": item["relevance_score"],
            "original_index": item["index"],
        })
    return results


if __name__ == "__main__":
    docs = [
        "RRF combines ranked lists using 1/(k+rank) without score normalization.",
        "HNSW builds a multi-layer graph for approximate nearest neighbor search.",
        "Cross-encoders jointly encode query and document for accurate reranking.",
    ]
    results = rerank("What is reciprocal rank fusion?", docs, top_n=2)
    for r in results:
        print(f"score={r['score']:.3f} | {r['text'][:60]}")