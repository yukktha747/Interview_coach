# RAG Fundamentals

## Q1: What is Retrieval-Augmented Generation and why is it needed?
RAG combines a retrieval system with a generative LLM so the model can ground its
answers in external, up-to-date, or proprietary documents instead of relying solely
on parametric knowledge learned during training. It reduces hallucination, allows
knowledge updates without retraining, and enables citation of sources.

**Rubric:** Answer should mention (1) grounding in external data, (2) avoiding
retraining for knowledge updates, (3) hallucination reduction. Bonus: mentions
citation/traceability.

---

## Q2: Walk through the chunking strategies you'd consider for a support-ticket
knowledge base, and their tradeoffs.
- **Fixed-size chunking**: simple, fast, but can split sentences/context mid-thought.
- **Sentence/paragraph-based**: preserves semantic units, variable chunk sizes.
- **Recursive character splitting**: falls back through separators (paragraph →
  sentence → word) to hit a target size while respecting structure.
- **Semantic chunking**: uses embedding similarity to find natural topic breaks;
  higher quality, more compute-expensive.
- **Document-aware chunking**: respects structure like headers, tables, code blocks.

**Rubric:** Should articulate the size/coherence tradeoff and pick something
appropriate for ticket data (short, structured, often has fields like
subject/body/resolution).

---

## Q3: What is hybrid retrieval and why combine BM25 with dense embeddings?
Hybrid retrieval combines sparse lexical search (BM25, good at exact keyword/term
matches, rare tokens, IDs, error codes) with dense embedding search (good at
semantic/paraphrase matches). Neither alone is sufficient: BM25 misses paraphrases,
dense embeddings can miss exact identifiers or rare technical terms.

**Rubric:** Must mention the complementary failure modes of each method.

---

## Q4: Explain Reciprocal Rank Fusion (RRF) and how it merges BM25 and dense results.
RRF combines ranked lists from multiple retrievers without needing to normalize raw
scores. For each document, its RRF score is the sum over each ranked list of
`1 / (k + rank)`, where `k` is a constant (commonly 60) that dampens the influence
of very high ranks. Documents appearing near the top of multiple lists get boosted.

```python
def reciprocal_rank_fusion(ranked_lists, k=60):
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

**Rubric:** Should explain why rank-based fusion avoids score-scale mismatch
between BM25 and cosine similarity.

---

## Q5: What is the role of a cross-encoder reranker in a RAG pipeline?
A cross-encoder (e.g., a Jina or Cohere reranker) jointly encodes the query and
each candidate document together, producing a relevance score that's far more
accurate than bi-encoder cosine similarity, at the cost of being too slow to run
over the full corpus. It's used as a second-stage filter: retrieve top-k (e.g. 50)
cheaply with dense/BM25, then rerank down to top-n (e.g. 5) with the cross-encoder.

**Rubric:** Must explain the two-stage retrieve-then-rerank pattern and why
cross-encoders aren't used for first-stage retrieval (latency/cost at scale).

---

## Q6: How do you reduce hallucination in a RAG system?
- Strong retrieval (better chunking, hybrid search, reranking) so the right context
  actually reaches the model.
- Prompting the model to answer only from provided context, and to say "I don't
  know" when context is insufficient.
- Citation-forcing: require the model to cite chunk IDs, making unsupported claims
  more visible.
- Post-hoc faithfulness checks (e.g., RAGAS faithfulness metric, NLI-based
  entailment checks) to flag ungrounded generations.

**Rubric:** Should distinguish retrieval-side fixes from generation-side fixes.

---

## Q7: How would you evaluate a RAG system end-to-end?
Using a framework like RAGAS, evaluate along multiple axes:
- **Context precision/recall**: is the retriever pulling the right chunks?
- **Faithfulness**: is the generated answer supported by the retrieved context?
- **Answer relevance**: does the answer actually address the question?

Retrieval and generation should be evaluated somewhat independently, since a
faithful-but-irrelevant answer points to a retrieval bug, while an unfaithful
answer with good retrieval points to a generation/prompting bug.

**Rubric:** Should separate retrieval metrics from generation metrics, not treat
RAG eval as one monolithic score.
