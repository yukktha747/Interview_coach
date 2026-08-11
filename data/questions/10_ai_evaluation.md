# AI / LLM Evaluation

## Q1: Why is LLM evaluation difficult?
LLM outputs are often open-ended, so correctness is not always a single exact string. Quality can involve relevance, factuality, completeness, style, safety, and task success.

**Rubric:** Should explain why exact-match testing is insufficient.

---

## Q2: What is retrieval evaluation?
Retrieval evaluation measures whether the system retrieves the information needed to answer a query. Metrics can include precision, recall, hit rate, and ranking-based measures.

**Rubric:** Should distinguish retrieval quality from generation quality.

---

## Q3: What is hallucination evaluation?
It checks whether generated claims are supported by trusted source information. Groundedness or faithfulness is particularly important in RAG applications.

**Rubric:** Should connect evaluation to evidence.

---

## Q4: What is an evaluation dataset?
It is a representative collection of inputs, expected behaviors, reference answers, relevant documents, or grading criteria used to measure system performance consistently.

**Rubric:** Should mention repeatable evaluation.

---

## Q5: Why are production traces useful?
Real traces reveal failure patterns that synthetic tests may miss. They can show bad retrieval, tool failures, latency problems, and unexpected user inputs.

**Rubric:** Should connect observability data to evaluation improvement.
