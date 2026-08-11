from crewai import Agent, Task, Crew, Process

from src.agents.tools import get_llm, search_knowledge_base

llm=get_llm()

interviewer = Agent(
    role="Technical Interviewer",
    goal=(
        "Ask one clear, focused interview question at a time from the "
        "knowledge base topic requested, and ask a relevant follow-up if the "
        "candidate's answer is vague or incomplete."
    ),
    backstory=(
        "You are an experienced AI/ML engineering interviewer. You ask "
        "questions the way a real technical interviewer would — clearly, "
        "without giving away the answer, and you probe deeper when responses "
        "are surface-level."
    ),
    tools=[search_knowledge_base],
    llm=llm,
    verbose=True,
)

evaluator = Agent(
    role="Answer Evaluator",
    goal=(
        "Grade the candidate's answer against the rubric for that question, "
        "retrieved from the knowledge base. Score 1-5 and justify the score "
        "with specific reference to what was missing or well-covered."
    ),
    backstory=(
        "You are a strict but fair technical grader. You never give full "
        "marks for vague or partially correct answers, and you always ground "
        "your evaluation in the retrieved rubric rather than your own opinion."
    ),
    tools=[search_knowledge_base],
    llm=llm,
    verbose=True,
)

coach = Agent(
    role="Interview Coach",
    goal=(
        "Given the evaluator's score and reasoning, give the candidate "
        "specific, actionable feedback: what to review, and one concrete "
        "way to strengthen their answer next time."
    ),
    backstory=(
        "You are a supportive but honest coach. You don't just praise — you "
        "point to the specific gap and suggest a concrete next study action, "
        "tied to the candidate's actual weak spot, not generic advice."
    ),
    llm=llm,
    verbose=True,
)


def run_interview_round(topic: str, candidate_answer: str):
    """
    One round: ask a question on `topic`, evaluate `candidate_answer` against
    it, then get coaching feedback. In a real session, ask_task's output
    would be shown to the user BEFORE they provide candidate_answer — this
    function assumes the answer is already given, useful for testing the
    pipeline end-to-end.
    """
    ask_task = Task(
        description=f"Ask one interview question about: {topic}. Use the knowledge base tool to find an appropriate question.",
        expected_output="A single clear interview question.",
        agent=interviewer,
    )

    evaluate_task = Task(
        description=(
            f"The candidate was asked a question about '{topic}' and answered:\n\n"
            f'"{candidate_answer}"\n\n'
            "Retrieve the rubric for this question from the knowledge base and "
            "score the answer 1-5, explaining what was missing or strong."
        ),
        expected_output="A score (1-5) and a specific justification referencing the rubric.",
        agent=evaluator,
        context=[ask_task],
    )

    coach_task = Task(
        description=(
            "Based on the evaluator's score and reasoning, give the candidate "
            "one specific, actionable piece of feedback on what to study next."
        ),
        expected_output="2-3 sentences of specific, actionable coaching feedback.",
        agent=coach,
        context=[evaluate_task],
    )

    crew = Crew(
        agents=[interviewer, evaluator, coach],
        tasks=[ask_task, evaluate_task, coach_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result


if __name__ == "__main__":
    # Quick end-to-end test with a deliberately incomplete answer
    result = run_interview_round(
        topic="reciprocal rank fusion",
        candidate_answer="RRF combines results from different search methods to get a better ranking.",
    )
    print("\n\n=== FINAL RESULT ===")
    print(result)