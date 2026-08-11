# LangGraph

## Q1: What is LangGraph?
LangGraph is a framework for building stateful, graph-based LLM workflows and agents. Nodes perform operations and edges determine how execution moves between them.

**Rubric:** Should mention graph structure and state.

---

## Q2: Why use a graph instead of a simple chain?
Graphs support branching, loops, conditional routing, retries, and more complex workflows. They are useful when an agent needs to make decisions about what happens next.

**Rubric:** Should explain control flow.

---

## Q3: What is state in an agent workflow?
State contains information shared across workflow steps, such as messages, tool results, intermediate decisions, or task status.

**Rubric:** Should explain why state is needed across nodes.

---

## Q4: How can you prevent infinite agent loops?
Use maximum iteration limits, explicit termination conditions, validation, and graph logic that guarantees or strongly encourages progress.

**Rubric:** Should provide concrete controls.

---

## Q5: When would you use a simple chain instead?
Use a chain when the workflow is mostly linear and deterministic. A graph is more appropriate when the workflow requires branching, iteration, or stateful decisions.

**Rubric:** Should show practical framework selection.
