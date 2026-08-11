# LLM Systems & Agentic AI

## Q1: What is KV caching and why does it matter for inference latency?
During autoregressive generation, each new token's attention computation needs the
key/value projections of all previous tokens. Without caching, you'd recompute
K/V for the entire sequence at every step — O(n²) total work. KV caching stores
these projections after they're first computed, so each new token only requires
one new K/V computation, reducing generation to O(n) incremental work. The
tradeoff is memory: KV cache size grows with sequence length and batch size, and
is often the actual bottleneck on GPU memory, not model weights.

**Rubric:** Should mention both the compute savings and the memory tradeoff.

---

## Q2: What is the difference between LangGraph and CrewAI, and when would you use
each?
- **LangGraph**: a low-level graph/state-machine framework for orchestrating
  control flow — nodes, edges, conditional routing, persistent state, cycles. Best
  when you need explicit control over *how* execution branches (retries, loops,
  human-in-the-loop checkpoints).
- **CrewAI**: a higher-level framework for defining role-based agent crews (e.g.
  "Researcher", "Writer", "Reviewer") that collaborate on a task with less
  boilerplate. Best when the problem naturally decomposes into agent *roles*
  rather than a custom state machine.

A common production pattern: use LangGraph for the top-level control flow, and
call a CrewAI crew from within a single LangGraph node when that step needs
multi-agent collaboration.

**Rubric:** Must distinguish control-flow orchestration (LangGraph) from
role-based agent collaboration (CrewAI), and ideally mention they can be
composed.

---

## Q3: What is the ReAct pattern in agentic systems?
ReAct (Reason + Act) interleaves explicit reasoning steps ("Thought: I need to look
up X") with tool-invoking actions ("Action: search(X)") and observations from the
tool's output, in a loop, until the agent decides it has enough information to
produce a final answer. This differs from a plain chain-of-thought prompt because
the reasoning is grounded by real tool outputs at each step, not just the model's
own generated text.

**Rubric:** Should describe the thought → action → observation loop structure.

---

## Q4: How do sampling parameters (temperature, top-p, top-k) affect LLM output,
and how would you tune them for an evaluator agent vs a creative writing agent?
- **Temperature**: scales the logits before softmax; higher = flatter distribution
  = more randomness.
- **Top-k**: restricts sampling to the k highest-probability tokens.
- **Top-p (nucleus)**: restricts sampling to the smallest set of tokens whose
  cumulative probability exceeds p.

For an **evaluator/grading agent**, you want low temperature (near 0) for
consistent, deterministic scoring. For a **creative writing agent**, higher
temperature and top-p allow more varied, less repetitive output.

**Rubric:** Should connect parameter choice to the specific agent's job, not just
define the terms.

---

## Q5: What is context window management, and what happens when an agentic loop
exceeds it?
The context window is the maximum number of tokens (input + output) a model can
process in a single call. In long agentic loops (many tool calls, growing message
history), you can exceed this limit. Strategies: summarizing older turns,
truncating/dropping low-relevance history, using a sliding window, or offloading
state to external memory (e.g., a vector store) and retrieving only what's
relevant to the current step.

**Rubric:** Should mention at least one concrete mitigation strategy, not just
"the context window is limited."

---

## Q6: What is data/model drift, and how would you detect it in a deployed
classifier?
Drift occurs when the statistical properties of incoming data (data drift) or the
relationship between inputs and the correct output (concept drift) change over
time relative to training data, degrading model performance silently. Detection
approaches: statistical tests comparing feature distributions over time (e.g.,
population stability index, KL divergence), monitoring prediction confidence
distributions, and tools like Evidently AI that automate distribution comparison
and alerting.

**Rubric:** Should distinguish data drift from concept drift and name at least one
detection method.

---

## Q7: Explain LoRA/QLoRA at a high level and why they're used for fine-tuning.
LoRA (Low-Rank Adaptation) freezes the pretrained model weights and injects small,
trainable low-rank matrices into specific layers (typically attention projections),
drastically reducing the number of trainable parameters compared to full
fine-tuning. QLoRA additionally quantizes the frozen base model to 4-bit precision,
further reducing memory requirements, allowing fine-tuning of large models on
consumer-grade GPUs.

**Rubric:** Should mention the frozen-base + low-rank-adapter mechanism, and for
QLoRA specifically, the quantization of the base model.

---

## Q8: How would you design an agentic system to avoid infinite loops or runaway
tool calls?
- Set a max iteration/step count in the graph or loop.
- Add explicit termination conditions (e.g., a "final_answer" tool that ends the
  loop when called).
- Track and detect repeated identical tool calls (same action, same input) as a
  stuck-loop signal.
- Use timeouts and cost/token budgets per session.
- Log and alert when the agent trace exceeds expected step counts, tying back into
  observability (e.g., MLflow tracing).

**Rubric:** Should give concrete guardrails, not just "add a max_steps parameter."
