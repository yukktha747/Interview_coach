# System Design Interview Framework

## Q1: What should you do first in a system design interview?
Clarify requirements before drawing architecture. Identify users, core functionality, scale, latency expectations, availability requirements, data characteristics, and important constraints.

**Rubric:** Should start with requirements rather than immediately naming technologies.

---

## Q2: How do you estimate scale?
Estimate users, requests per second, peak traffic, data growth, payload sizes, storage requirements, and read/write ratios. Exact numbers are less important than showing reasonable assumptions.

**Rubric:** Should demonstrate structured estimation.

---

## Q3: What is a basic architecture flow?
A common flow is client → load balancer/API gateway → application services → cache/database/queue/external services. The exact components depend on requirements.

**Rubric:** Should explain components and request flow.

---

## Q4: How do you discuss tradeoffs?
For each major decision, explain why it fits the requirements and what downside it introduces. Examples include consistency vs availability, latency vs cost, simplicity vs flexibility, and recall vs speed.

**Rubric:** Should explicitly discuss tradeoffs.

---

## Q5: What should the final part of the interview cover?
Review bottlenecks, failure scenarios, scaling strategy, security, observability, data consistency, and possible future improvements.

**Rubric:** Should end with reliability and scalability rather than only the happy path.
