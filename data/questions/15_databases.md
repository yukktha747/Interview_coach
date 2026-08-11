# Databases for AI Systems

## Q1: Why might an AI application use multiple databases?
Different workloads have different requirements. A relational database can handle structured transactional data, a vector database can handle similarity search, object storage can hold files, and a cache can provide fast temporary access.

**Rubric:** Should explain polyglot persistence by workload.

---

## Q2: When would you use SQL?
SQL databases are useful for structured data, transactions, relationships, constraints, and queries that require strong consistency and predictable schemas.

**Rubric:** Should mention transactional workloads.

---

## Q3: When would you use object storage?
Object storage is appropriate for large files such as PDFs, images, videos, datasets, and raw document versions.

**Rubric:** Should distinguish files from transactional metadata.

---

## Q4: Why keep metadata separately from embeddings?
Metadata such as document ID, tenant, category, permissions, timestamps, and source information supports filtering, authorization, updates, and traceability.

**Rubric:** Should connect metadata to retrieval and system correctness.

---

## Q5: What is database indexing?
An index is an auxiliary data structure that helps the database find records efficiently without scanning every row.

**Rubric:** Should explain the purpose as faster lookup.
