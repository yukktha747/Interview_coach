# AI Security

## Q1: What is prompt injection?
Prompt injection occurs when untrusted content attempts to influence the model into ignoring intended instructions or performing unintended actions.

**Rubric:** Should distinguish untrusted data from trusted system instructions.

---

## Q2: Why is RAG vulnerable to prompt injection?
Retrieved documents may contain instructions that look like commands. If the application blindly places them into a prompt, the model may treat those instructions as authoritative.

**Rubric:** Should explain the trust-boundary problem.

---

## Q3: What is least privilege for AI agents?
An agent should receive only the permissions and tools required for its task. It should not automatically have broad access to databases, files, or external systems.

**Rubric:** Should connect permissions to blast-radius reduction.

---

## Q4: How should secrets be handled?
API keys and credentials should be stored in secure secret-management systems or protected environment configuration rather than hardcoded into prompts, source code, or client applications.

**Rubric:** Should mention avoiding hardcoded secrets.

---

## Q5: Why log tool calls?
Tool-call logs help detect misuse, debug failures, audit actions, and understand agent behavior.

**Rubric:** Should connect logging to security and observability.
