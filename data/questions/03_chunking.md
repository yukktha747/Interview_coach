# Chunking Strategy

## Q1: What is chunking?
Chunking is the process of splitting large documents into smaller pieces before embedding and retrieval. The goal is to create chunks that are small enough for precise retrieval but large enough to preserve useful context.

**Rubric:** Should explain the precision/context tradeoff.

---

## Q2: What are chunk size and chunk overlap?
Chunk size controls how much text is placed in each chunk. Chunk overlap repeats a small amount of text between adjacent chunks so important information near a boundary is less likely to be separated.

**Rubric:** Should distinguish size from overlap.

---

## Q3: Why not use extremely small chunks?
Very small chunks may lose context and produce incomplete answers. They can also increase the number of retrieved chunks and make context assembly harder.

**Rubric:** Should mention loss of context.

---

## Q4: Why not use extremely large chunks?
Large chunks may contain unrelated information, reduce retrieval precision, consume more context-window tokens, and increase LLM cost.

**Rubric:** Should mention precision and token-cost tradeoffs.

---

## Q5: How do you choose chunking strategy?
Start with document structure and use headings, paragraphs, sections, or semantic boundaries where possible. Then evaluate retrieval quality using representative questions rather than relying on a fixed chunk size.

**Rubric:** Should emphasize evaluation instead of blindly choosing one size.
