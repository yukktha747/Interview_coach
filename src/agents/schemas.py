from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """
    Structured output contract for the Evaluator agent. Replacing the old
    'scan the text for a digit 1-5' extraction with actual schema validation —
    if the LLM's output doesn't conform (wrong type, score out of range,
    missing field), this raises a validation error we can catch and retry,
    instead of silently guessing wrong.
    """
    score: int = Field(ge=1, le=5, description="Score from 1 (poor) to 5 (excellent)")
    justification: str = Field(min_length=10, description="Specific reasoning referencing the rubric")
    missing_points: list[str] = Field(
        default_factory=list,
        description="Specific concepts from the rubric the candidate's answer failed to mention",
    )