# API Design

## Q1: What makes an API well designed?
A good API has clear resources or operations, predictable request/response schemas, meaningful status codes, authentication, validation, consistent errors, and documented behavior.

**Rubric:** Should mention consistency and validation.

---

## Q2: Why validate API inputs?
Validation prevents malformed or unsafe data from reaching downstream services. In AI applications it is especially important because model-generated tool arguments should not automatically be trusted.

**Rubric:** Should connect validation to both reliability and security.

---

## Q3: What is pagination?
Pagination divides a large result set into smaller responses. It prevents a single request from returning excessive data and consuming too many resources.

**Rubric:** Should explain scalability benefits.

---

## Q4: Why use timeouts?
A timeout prevents a request from waiting indefinitely for a slow dependency. It helps free resources and allows controlled failure handling.

**Rubric:** Should connect timeouts to resource protection.

---

## Q5: What is an API rate limit?
A rate limit restricts how many requests a client can make within a time period. It protects services from abuse and traffic spikes.

**Rubric:** Should mention protection and fairness.
