# Load Balancing

## Q1: Why use a load balancer?
A load balancer distributes incoming traffic across multiple healthy instances, improving availability and allowing horizontal scaling.

**Rubric:** Should mention both scaling and availability.

---

## Q2: What is round-robin?
Round-robin distributes requests sequentially across available servers.

**Rubric:** Should explain the basic distribution strategy.

---

## Q3: What is health checking?
The load balancer periodically checks whether service instances are healthy. Unhealthy instances can be removed from request routing.

**Rubric:** Should connect health checks to fault isolation.

---

## Q4: What is sticky session routing?
Sticky sessions try to route a client's requests to the same backend instance. They can simplify session handling but reduce flexibility in scaling and failover.

**Rubric:** Should mention the tradeoff.

---

## Q5: Why prefer stateless services?
Stateless services allow requests to be routed to any healthy instance, making horizontal scaling and failure recovery simpler.

**Rubric:** Should connect statelessness to load balancing.
