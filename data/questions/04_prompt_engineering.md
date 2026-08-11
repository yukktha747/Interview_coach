# Prompt Engineering

## Q1: What is prompt engineering?
Prompt engineering is the design of instructions, context, constraints, examples, and output formats that guide an LLM toward a desired behavior.

**Rubric:** Should describe prompts as structured instructions, not magic keywords.

---

## Q2: What is zero-shot prompting?
Zero-shot prompting asks the model to perform a task without providing examples. The instructions describe what the model should do and what output is expected.

**Rubric:** Should distinguish it from few-shot prompting.

---

## Q3: What is few-shot prompting?
Few-shot prompting provides a small number of input-output examples so the model can infer the desired pattern, format, or behavior.

**Rubric:** Should mention examples as guidance.

---

## Q4: Why use structured output?
Structured output such as JSON makes model responses easier for software to parse and validate. It reduces ambiguity when the LLM is part of an application pipeline.

**Rubric:** Should connect structured output to application reliability.

---

## Q5: What makes a production prompt robust?
Clear instructions, explicit constraints, relevant context, defined failure behavior, examples where useful, and output validation. Prompts should also be tested against adversarial and edge-case inputs.

**Rubric:** Should mention validation and edge cases.
