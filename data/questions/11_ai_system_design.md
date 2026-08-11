# AI System Design Basics

## Q1: What are the major components of an AI application?
A typical system may contain an API layer, authentication, application/orchestration service, LLM provider, embedding service, vector database, relational/document database, cache, object storage, queue, and observability layer.

**Rubric:** Should show that AI systems still depend on standard distributed-system components.

---

## Q2: Where should the LLM call happen?
Usually inside an application/orchestration service that handles prompts, context retrieval, tool calls, validation, retries, and business rules rather than exposing the model provider directly to clients.

**Rubric:** Should mention separation between client and model provider.

---

## Q3: Why use a queue?
Queues decouple producers and consumers and are useful for asynchronous tasks such as document ingestion, embedding generation, batch processing, and long-running agent jobs.

**Rubric:** Should connect queues to decoupling and asynchronous processing.

---

## Q4: Why add caching?
Caching can reduce repeated expensive LLM, embedding, database, or retrieval operations and improve latency. The system needs a sensible cache key and invalidation strategy.

**Rubric:** Should mention latency/cost and invalidation.

---

## Q5: What should you monitor?
Track latency, error rate, token usage, model/provider failures, retrieval quality, cache hit rate, queue depth, tool failures, and application-level success metrics.

**Rubric:** Should cover both infrastructure and AI-specific metrics.
