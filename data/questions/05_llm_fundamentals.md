# LLM Fundamentals

## Q1: What is an LLM?
A Large Language Model is a neural network trained on large amounts of data to predict and generate sequences of tokens. Modern LLMs commonly use Transformer architectures.

**Rubric:** Should connect token prediction to language generation.

---

## Q2: What is a token?
A token is a unit processed by the language model. Depending on the tokenizer, a token can represent a word, part of a word, punctuation, or another text fragment.

**Rubric:** Should not equate tokens directly with words.

---

## Q3: What is attention?
Attention allows a model to weigh the importance of different tokens when processing a sequence. This helps the model capture relationships between words or concepts that may be far apart.

**Rubric:** Should explain attention as selective interaction between tokens.

---

## Q4: What is temperature?
Temperature controls how strongly the model favors high-probability tokens during sampling. Lower values generally make output more deterministic, while higher values increase variation.

**Rubric:** Should connect temperature to randomness/variation.

---

## Q5: What is hallucination?
Hallucination is when an LLM produces information that sounds plausible but is unsupported, incorrect, or fabricated.

**Rubric:** Should distinguish fluent output from factual correctness.
