# Fine-Tuning and Parameter-Efficient Fine-Tuning

## Q1: What is fine-tuning?
Fine-tuning adapts a pretrained model by training it further on task- or domain-specific data. The model's parameters are updated so it becomes better suited to the target behavior.

**Rubric:** Should distinguish adaptation from training from scratch.

---

## Q2: What is LoRA?
LoRA freezes the original model weights and trains small low-rank adapter matrices. This dramatically reduces the number of parameters that need to be trained.

**Rubric:** Should mention frozen base weights and trainable low-rank adapters.

---

## Q3: What is QLoRA?
QLoRA combines a quantized base model with LoRA adapters. The base model uses reduced-precision storage while the adapters remain trainable, reducing memory requirements for fine-tuning.

**Rubric:** Should distinguish QLoRA from ordinary LoRA.

---

## Q4: When should you use RAG instead of fine-tuning?
Use RAG when the main problem is access to changing or private knowledge. Fine-tuning is more appropriate when you want to change behavior, style, task performance, or output patterns.

**Rubric:** Should explain knowledge retrieval vs behavior adaptation.

---

## Q5: What is a fine-tuning risk?
Poor training data can teach the model incorrect behavior or cause overfitting. Fine-tuning can also make maintenance harder if the underlying knowledge changes frequently.

**Rubric:** Should mention data quality and maintenance.
