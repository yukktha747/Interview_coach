# Caching

## Q1: What is caching?
Caching stores frequently accessed or expensive-to-compute data in a faster storage layer so future requests can be served more quickly.

**Rubric:** Should mention latency and repeated work.

---

## Q2: What is cache-aside?
The application first checks the cache. On a miss, it reads from the source database, returns the result, and populates the cache.

**Rubric:** Should describe the miss path.

---

## Q3: What is cache invalidation?
Cache invalidation removes or updates stale cached data when the underlying source changes.

**Rubric:** Should recognize stale data as the central challenge.

---

## Q4: What is a cache stampede?
A cache stampede happens when many requests simultaneously miss an expired cache entry and all hit the backend.

**Rubric:** Should mention synchronized backend load.

---

## Q5: How can you reduce cache stampedes?
Use TTL jitter, request coalescing, locks, stale-while-revalidate behavior, or proactive refresh depending on the workload.

**Rubric:** Should provide at least two concrete strategies.
