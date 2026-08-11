import os
import requests
from dotenv import load_dotenv

from src.utils.retry import retry_with_backoff
from src.utils.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)

JINA_API_KEY = os.getenv("JINA_API_KEY")
JINA_EMBED_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v3"  # confirm this matches what you used previously


@retry_with_backoff(max_attempts=3, exceptions=(requests.exceptions.RequestException,))
def embed_texts(texts: list[str], task: str = "retrieval.passage") -> list[list[float]]:
    """
    Embed a list of texts using Jina's embedding API.
    task: 'retrieval.passage' for documents being indexed,
          'retrieval.query' for search queries (asymmetric embedding).
    """
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY not found in environment")

    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": JINA_MODEL,
        "task": task,
        "input": texts,
    }

    logger.info(f"Embedding {len(texts)} text(s) (task={task})")
    response = requests.post(JINA_EMBED_URL, headers=headers, json=payload)

    if response.status_code == 429:
        logger.warning("Jina embeddings API rate limited (429)")
    response.raise_for_status()
    data = response.json()

    sorted_data = sorted(data["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in sorted_data]


if __name__ == "__main__":
    vecs = embed_texts(["What is RRF?", "Explain KV caching"])
    print(f"Got {len(vecs)} embeddings, dim={len(vecs[0])}")