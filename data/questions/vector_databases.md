# Vector Databases

## Q1: What is an ANN (Approximate Nearest Neighbor) index and why not use exact
search?
Exact k-NN requires comparing a query vector against every vector in the
collection — O(n) per query — which doesn't scale past a few hundred thousand
vectors with low latency requirements. ANN indexes (HNSW, IVF, LSH) trade a small
amount of recall for massive speedups by organizing vectors into searchable
structures (graphs, clusters, hash buckets) that let you skip most comparisons.

**Rubric:** Should mention the recall/speed tradeoff explicitly.

---

## Q2: Explain how HNSW (Hierarchical Navigable Small World) works at a high level.
HNSW builds a multi-layer graph where each vector is a node. Upper layers are
sparse with long-range links (fast traversal across the space), lower layers are
dense with short-range links (fine-grained accuracy). A query starts at the top
layer, greedily walks toward the closest node, then descends layer by layer,
refining the search. This gives logarithmic-ish search complexity.

**Rubric:** Should mention the layered structure and greedy graph traversal;
doesn't need exact complexity proofs.

---

## Q3: What is the difference between Qdrant and Chroma, and when would you pick
one over the other?
- **Chroma**: lightweight, embedded or lightly-served, great for local dev,
  prototyping, and small-to-medium datasets. Simple Python API.
- **Qdrant**: production-grade, written in Rust, supports payload filtering,
  clustering/sharding, quantization, and higher throughput at scale. Better suited
  for production deployments with millions of vectors and complex metadata
  filtering needs.

**Rubric:** Should articulate a dev/prototype vs production distinction, not just
"they're both vector DBs."

---

## Q4: How do incremental upserts work, and why do they matter for a support-ticket
knowledge base?
Support tickets get resolved, updated, or closed continuously — the knowledge base
isn't static. Incremental upserts let you add or update individual vectors (and
their metadata/payload) without re-indexing the entire collection. This requires
stable, deterministic document IDs (e.g., hash of ticket ID + chunk index) so that
re-ingesting an updated ticket overwrites the old chunk rather than duplicating it.

**Rubric:** Must mention deterministic ID strategy as the key mechanism enabling
safe upserts.

---

## Q5: What is vector quantization and why would you use it?
Quantization compresses vectors (e.g., float32 → int8, or product quantization
into subvector codebooks) to reduce memory footprint and speed up distance
computation, at some cost to recall accuracy. Useful when the collection is large
enough that keeping full-precision vectors in memory becomes expensive.

**Rubric:** Should mention the memory/latency vs accuracy tradeoff.

---

## Q6: How do you optimize vector DB query latency in production?
- Tune HNSW parameters (`ef_search`, `m`) to balance recall vs speed.
- Use metadata filtering to narrow the search space before/during ANN search.
- Apply quantization for memory-bound workloads.
- Cache frequent queries.
- Shard/replicate the collection horizontally for high QPS.
- Reduce embedding dimensionality if the embedding model allows it (e.g., Matryoshka
  embeddings) without significant recall loss.

**Rubric:** Should give at least 3 concrete levers, not just "scale horizontally."

---

## Q7: What metadata filtering strategies matter for a ticket knowledge base?
Filtering by fields like `category`, `priority`, `resolved_status`, `product_area`,
or `date_range` before/during vector search lets you narrow retrieval to relevant
subsets (e.g., only "billing" category tickets) rather than relying purely on
semantic similarity, which improves both precision and latency.

**Rubric:** Should connect filtering to precision improvement, not just speed.
