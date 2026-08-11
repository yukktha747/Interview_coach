import os
import uuid
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

from src.indexing.embeddings import embed_texts

load_dotenv()

COLLECTION_NAME = "interview_questions"
VECTOR_DIM = 1024  


def get_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )


def deterministic_id(text: str, source_file: str) -> str:
    """
    Stable ID derived from content + source, so re-ingesting the same
    chunk upserts (overwrites) instead of duplicating. Ties back to the
    incremental-upsert question in your own vector_databases.md Q4.
    """
    raw = f"{source_file}:{text[:100]}"
    return str(uuid.UUID(hashlib.md5(raw.encode()).hexdigest()))


def ensure_collection(client: QdrantClient):
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )


def upsert_nodes(nodes: list):
    """
    nodes: list of LlamaIndex Node objects from loader.load_and_chunk()
    """
    client = get_client()
    ensure_collection(client)

    texts = [node.text for node in nodes]
    vectors = embed_texts(texts, task="retrieval.passage")

    points = []
    for node, vector in zip(nodes, vectors):
        source_file = node.metadata.get("file_name", "unknown")
        point_id = deterministic_id(node.text, source_file)
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": node.text,
                    "source_file": source_file,
                },
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Upserted {len(points)} points into '{COLLECTION_NAME}'")


def search(query: str, top_k: int = 5):
    client = get_client()
    query_vector = embed_texts([query], task="retrieval.query")[0]
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )
    return results.points


def search_with_rerank(query: str, first_stage_k: int = 8, final_k: int = 3) -> list[dict]:
    """
    Two-stage retrieval: cheap dense search over a wider candidate set
    (first_stage_k), then a cross-encoder reranker narrows it down to the
    most relevant final_k. See rag_fundamentals.md Q5 for the reasoning.
    """
    from src.indexing.reranker import rerank

    candidates = search(query, top_k=first_stage_k)
    if not candidates:
        return []

    candidate_texts = [c.payload["text"] for c in candidates]
    reranked = rerank(query, candidate_texts, top_n=final_k)
    return reranked  # list of {"text", "score", "original_index"}


if __name__ == "__main__":
    from src.ingestion.loader import load_and_chunk

    nodes = load_and_chunk()
    upsert_nodes(nodes)

    results = search("What is reciprocal rank fusion?")
    for r in results:
        print(f"score={r.score:.3f} | {r.payload['text'][:100]}")