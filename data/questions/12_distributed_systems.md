# Distributed Systems Basics

## Q1: What is horizontal scaling?
Horizontal scaling means adding more instances of a service instead of relying on one larger machine. A load balancer distributes requests across instances.

**Rubric:** Should distinguish horizontal from vertical scaling.

---

## Q2: What is load balancing?
A load balancer distributes incoming traffic across healthy service instances. It can improve availability, capacity, and fault tolerance.

**Rubric:** Should mention traffic distribution and health.

---

## Q3: What is a stateless service?
A stateless service does not depend on local instance memory to maintain client session state. This makes instances easier to scale and replace.

**Rubric:** Should connect statelessness to horizontal scaling.

---

## Q4: What is a retry problem?
Retries can help recover from transient failures, but uncontrolled retries can overload an already struggling dependency. Exponential backoff and retry limits are common safeguards.

**Rubric:** Should mention retry storms and backoff.

---

## Q5: What is idempotency?
An operation is idempotent when repeating the same request produces the same intended result. Idempotency keys are often used to prevent duplicate effects during retries.

**Rubric:** Should connect idempotency to distributed retries.
