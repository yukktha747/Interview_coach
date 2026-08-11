# Retrieval-Augmented Generation (RAG)

## Q1: What is RAG?
RAG combines retrieval with generation. The system first retrieves relevant information from an external knowledge source and then provides that information to an LLM as context for generating the answer.

**Rubric:** Should clearly describe retrieval followed by generation.

---

## Q2: Why use RAG instead of putting all documents in the prompt?
RAG avoids sending the entire knowledge base on every request. It reduces context size, cost, latency, and irrelevant information while allowing the knowledge source to be updated independently of the model.

**Rubric:** Should mention scalability and freshness.

---

## Q3: What is the basic RAG pipeline?
A typical pipeline is: ingest documents → clean them → chunk them → create embeddings → store vectors and metadata → embed the query → retrieve candidates → optionally rerank → construct the prompt → generate the answer.

**Rubric:** Should cover both indexing and query-time stages.

---

## Q4: What is a common RAG failure?
A common failure is poor retrieval. If the correct information is not retrieved, even a strong LLM may generate an incorrect answer because it was not given the required context.

**Rubric:** Should recognize that generation quality depends on retrieval quality.

---

## Q5: How do you improve RAG quality?
Improve chunking, embeddings, metadata filters, retrieval parameters, reranking, query rewriting, context selection, and evaluation. Also ensure the source documents are clean and current.

**Rubric:** Should give multiple concrete retrieval and generation levers.
