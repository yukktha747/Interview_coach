# Embeddings

## Q1: What is an embedding?
An embedding is a dense numerical vector that represents the semantic meaning of data such as text, images, or code. Similar concepts are mapped to nearby points in vector space, which makes embeddings useful for semantic search, recommendation, clustering, and retrieval.

**Rubric:** Should explain that embeddings represent meaning as vectors, not just keywords.

---

## Q2: Why are embeddings useful in RAG?
Embeddings allow documents and queries to be represented in the same vector space. A query can therefore retrieve chunks that are semantically related even when the exact words do not match.

**Rubric:** Should connect embeddings to semantic retrieval.

---

## Q3: What is embedding dimensionality?
Dimensionality is the number of numerical values in each embedding vector. Higher dimensions can represent more information but increase memory usage, storage, and distance-computation cost.

**Rubric:** Should mention the accuracy/resource tradeoff.

---

## Q4: What is cosine similarity?
Cosine similarity measures the angle between two vectors. Values closer to 1 indicate that the vectors point in similar directions, while values closer to 0 indicate little directional similarity.

**Rubric:** Should explain it as a measure of vector similarity.

---

## Q5: What happens if you change the embedding model?
Existing vectors generally need to be re-embedded because vectors from different models are not guaranteed to occupy the same vector space. Mixing incompatible embeddings can produce incorrect retrieval.

**Rubric:** Should mention re-embedding and vector-space compatibility.
