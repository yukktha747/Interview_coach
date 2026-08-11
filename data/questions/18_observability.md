# Observability for AI Systems

## Q1: What is observability?
Observability is the ability to understand the internal behavior of a system from its outputs and telemetry. Common signals include logs, metrics, and traces.

**Rubric:** Should mention logs, metrics, and traces.

---

## Q2: What should you log for an LLM request?
Useful fields include request ID, model, latency, token counts, retrieval information, tool calls, errors, and outcome metrics. Sensitive user data should be handled carefully.

**Rubric:** Should balance debugging value with privacy.

---

## Q3: What is distributed tracing?
Distributed tracing follows a request across multiple services so engineers can identify where latency or failures occur.

**Rubric:** Should connect tracing to multi-service debugging.

---

## Q4: What AI-specific metrics matter?
Token usage, cost, time-to-first-token, total latency, retrieval hit rate, tool failure rate, hallucination/groundedness signals, and task success can be important.

**Rubric:** Should include AI-specific metrics rather than only CPU/memory.

---

## Q5: Why use correlation IDs?
A correlation ID allows logs and traces from different services involved in the same request to be connected.

**Rubric:** Should explain cross-service request tracking.
