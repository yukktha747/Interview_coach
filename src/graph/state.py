from typing import TypedDict, Optional


class InterviewState(TypedDict):
    topic: str                      # current topic being asked about, e.g. "reciprocal rank fusion"
    current_question: str           # the question the Interviewer just asked
    candidate_answer: Optional[str] # filled in once the human responds; None while waiting
    score: Optional[int]            # 1-5, filled in after evaluation
    evaluation_reasoning: str       # Evaluator's justification
    coach_feedback: str             # Coach's actionable feedback
    weak_topics: list[str]          # topics where score was low, accumulated across rounds
    round_number: int               # which round of the session we're on
    max_rounds: int                 # when to end the session
    topics_pool: list[str]          # topics available to pull from
    question_context: list[str]     # KB chunks retrieved to generate the question (for RAGAS)
    evaluation_context: list[str]   # KB chunks retrieved to grade the answer (for RAGAS)
    session_log: list[dict]         # accumulated record of every round, for post-session RAGAS eval