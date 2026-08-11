# Message Queues

## Q1: Why use a message queue?
Queues decouple services and allow work to be processed asynchronously. They are useful for workloads that do not need to finish during the original HTTP request.

**Rubric:** Should mention decoupling and asynchronous processing.

---

## Q2: What is a producer and consumer?
A producer publishes messages. A consumer reads and processes those messages.

**Rubric:** Should clearly distinguish the two roles.

---

## Q3: What happens if a consumer fails?
Depending on the queue system, the message can remain available or be retried. Dead-letter queues can isolate messages that repeatedly fail.

**Rubric:** Should mention retries and dead-letter handling.

---

## Q4: What is at-least-once delivery?
At-least-once delivery means a message may be delivered more than once, so consumers should be designed to tolerate duplicates.

**Rubric:** Should connect delivery semantics to idempotency.

---

## Q5: Why are queues useful in AI systems?
They can handle document ingestion, embedding generation, batch evaluation, asynchronous agent jobs, and other workloads that may be slow or bursty.

**Rubric:** Should give AI-specific examples.
