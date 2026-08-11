# AI Agents

## Q1: What is an AI agent?
An AI agent is a system in which an LLM can reason about a goal, decide what action to take, use tools or external systems, observe results, and continue until the task is completed or stopped.

**Rubric:** Should include tools/actions and feedback, not just conversation.

---

## Q2: How is an agent different from a chatbot?
A chatbot primarily responds to messages. An agent can take actions such as calling APIs, searching databases, executing workflows, or using tools based on the task.

**Rubric:** Should emphasize action and tool use.

---

## Q3: What is the agent loop?
A simplified loop is: receive goal → reason/plan → choose tool/action → execute → observe result → decide next action → finish.

**Rubric:** Should explain the feedback loop.

---

## Q4: Why can agents be unreliable?
Agents can choose incorrect tools, make poor plans, loop indefinitely, misuse permissions, or interpret tool results incorrectly.

**Rubric:** Should mention operational and reasoning failure modes.

---

## Q5: How do you make agents safer?
Use tool permissions, validation, timeouts, iteration limits, structured tool inputs, human approval for high-impact actions, logging, and evaluation.

**Rubric:** Should mention guardrails and observability.
