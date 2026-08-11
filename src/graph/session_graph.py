import time

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

from src.graph.state import InterviewState
from src.agents.crew import interviewer, evaluator, coach
from src.agents.schemas import EvaluationResult
from src.indexing.qdrant_store import search_with_rerank
from src.utils.logging_config import get_logger
from crewai import Task, Crew, Process
from pydantic import ValidationError

logger = get_logger(__name__)


def _retrieve_texts(query: str, top_k: int = 3) -> list[str]:
    """
    Explicit retrieval so we know exactly what context was used — separate
    from the agent's own tool-calling, which we can't fully observe.
    Uses two-stage retrieve-then-rerank: wider first-stage candidate pool,
    narrowed by a cross-encoder reranker.

    Returns an empty list on failure rather than raising — a node that
    can't retrieve context should still be able to fall back gracefully
    (e.g. ask a generic question) instead of crashing the whole session.
    """
    try:
        results = search_with_rerank(query, first_stage_k=8, final_k=top_k)
        return [r["text"] for r in results]
    except Exception as e:
        logger.error(f"Retrieval failed for query {query[:50]!r}: {e}")
        return []


# ---------- Node 0: pause and let the human pick a topic ----------
def select_topic_node(state: InterviewState) -> dict:
    chosen_topic = interrupt({
        "type": "select_topic",
        "topics_pool": state["topics_pool"],
        "weak_topics": state["weak_topics"],
    })
    return {"topic": chosen_topic}


# ---------- Node 1: ask a question ----------
def ask_question_node(state: InterviewState) -> dict:
    topic = state["topic"]
    context_chunks = _retrieve_texts(topic)
    context_str = "\n\n---\n\n".join(context_chunks) if context_chunks else "(no context retrieved)"

    start = time.time()
    try:
        ask_task = Task(
            description=(
                f"Using ONLY this retrieved context, ask one clear interview "
                f"question about {topic}:\n\n{context_str}"
            ),
            expected_output="A single clear interview question.",
            agent=interviewer,
        )
        crew = Crew(agents=[interviewer], tasks=[ask_task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        question = str(result)
        logger.info(f"Round {state['round_number'] + 1}: generated question for topic {topic!r}")
    except Exception as e:
        logger.error(f"Interviewer agent failed for topic {topic!r}: {e}")
        question = (
            f"(Fallback question — the Interviewer agent hit an error) "
            f"Can you explain the key concept behind {topic}?"
        )
    latency_ms = (time.time() - start) * 1000
    logger.info(f"ask_question_node took {latency_ms:.0f}ms")

    return {
        "current_question": question,
        "round_number": state["round_number"] + 1,
        "question_context": context_chunks,
    }


# ---------- Node 2: pause and wait for the human's real answer ----------
def collect_answer_node(state: InterviewState) -> dict:
    answer = interrupt({
        "type": "collect_answer",
        "question": state["current_question"],
        "topic": state["topic"],
    })
    return {"candidate_answer": answer}


# ---------- Node 3: evaluate the answer against the rubric ----------
def evaluate_node(state: InterviewState) -> dict:
    context_chunks = _retrieve_texts(state["current_question"])
    context_str = "\n\n---\n\n".join(context_chunks) if context_chunks else "(no context retrieved)"

    start = time.time()
    score = None
    justification = ""
    missing_points = []

    MAX_VALIDATION_ATTEMPTS = 2
    for attempt in range(1, MAX_VALIDATION_ATTEMPTS + 1):
        try:
            evaluate_task = Task(
                description=(
                    f"The candidate was asked: '{state['current_question']}'\n"
                    f"They answered: \"{state['candidate_answer']}\"\n\n"
                    f"Here is the retrieved rubric context:\n\n{context_str}\n\n"
                    "Using ONLY this context, score the answer, explain what was "
                    "missing or strong, and list any specific rubric points the "
                    "candidate's answer failed to cover."
                ),
                expected_output=(
                    "A JSON object with fields: score (int 1-5), justification "
                    "(string), missing_points (list of strings)."
                ),
                agent=evaluator,
                output_pydantic=EvaluationResult,
            )
            crew = Crew(agents=[evaluator], tasks=[evaluate_task], process=Process.sequential, verbose=False)
            crew_output = crew.kickoff()

            parsed = crew_output.pydantic
            if parsed is None:
                raise ValidationError.from_exception_data(
                    "EvaluationResult", [{"type": "missing", "loc": ("root",), "input": str(crew_output)}]
                )

            score = parsed.score
            justification = parsed.justification
            missing_points = parsed.missing_points
            logger.info(
                f"Evaluated round {state['round_number']} on attempt {attempt}: "
                f"score={score}, missing_points={len(missing_points)}"
            )
            break

        except (ValidationError, Exception) as e:
            logger.warning(
                f"Evaluator output failed schema validation on attempt "
                f"{attempt}/{MAX_VALIDATION_ATTEMPTS}: {e}"
            )
            if attempt == MAX_VALIDATION_ATTEMPTS:
                logger.error("Evaluator exhausted validation retries — falling back")
                score = None
                justification = (
                    "(Evaluation unavailable — the Evaluator agent's output "
                    "failed schema validation after retries. Your answer was "
                    "recorded but could not be reliably scored this round.)"
                )

    latency_ms = (time.time() - start) * 1000
    logger.info(f"evaluate_node took {latency_ms:.0f}ms")
    evaluation_reasoning = justification
    if missing_points:
        evaluation_reasoning += "\n\nMissing: " + "; ".join(missing_points)

    return {
        "score": score,
        "evaluation_reasoning": evaluation_reasoning,
        "evaluation_context": context_chunks,
    }


# ---------- Node 4: coach feedback ----------
def coach_node(state: InterviewState) -> dict:
    start = time.time()
    try:
        coach_task = Task(
            description=(
                f"The candidate scored {state['score']}/5 on a question about "
                f"'{state['topic']}'. Evaluator reasoning: {state['evaluation_reasoning']}\n\n"
                "Give one specific, actionable piece of feedback on what to study next."
            ),
            expected_output="2-3 sentences of specific, actionable coaching feedback.",
            agent=coach,
        )
        crew = Crew(agents=[coach], tasks=[coach_task], process=Process.sequential, verbose=False)
        result = str(crew.kickoff())
    except Exception as e:
        logger.error(f"Coach agent failed: {e}")
        result = (
            "(Coaching feedback unavailable this round — the Coach agent hit an error. "
            "Review the rubric for this topic directly in the meantime.)"
        )
    latency_ms = (time.time() - start) * 1000
    logger.info(f"coach_node took {latency_ms:.0f}ms")

    weak_topics = state["weak_topics"]
    if state["score"] is not None and state["score"] <= 3 and state["topic"] not in weak_topics:
        weak_topics = weak_topics + [state["topic"]]

    round_record = {
        "topic": state["topic"],
        "question": state["current_question"],
        "question_context": state["question_context"],
        "answer": state["candidate_answer"],
        "evaluation_context": state["evaluation_context"],
        "evaluation_reasoning": state["evaluation_reasoning"],
        "score": state["score"],
        "coach_feedback": result,
    }
    session_log = state["session_log"] + [round_record]

    return {
        "coach_feedback": result,
        "weak_topics": weak_topics,
        "session_log": session_log,
    }


# ---------- Conditional edge: continue or end the session ----------
def should_continue(state: InterviewState) -> str:
    if state["round_number"] >= state["max_rounds"]:
        return "end"
    return "continue"


def build_graph():
    graph = StateGraph(InterviewState)

    graph.add_node("select_topic", select_topic_node)
    graph.add_node("ask_question", ask_question_node)
    graph.add_node("collect_answer", collect_answer_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("coach", coach_node)

    graph.set_entry_point("select_topic")
    graph.add_edge("select_topic", "ask_question")
    graph.add_edge("ask_question", "collect_answer")
    graph.add_edge("collect_answer", "evaluate")
    graph.add_edge("evaluate", "coach")

    graph.add_conditional_edges(
        "coach",
        should_continue,
        {"continue": "select_topic", "end": END},
    )

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    import json

    app = build_graph()
    config = {"configurable": {"thread_id": "session-1"}}

    initial_state = {
        "topic": "",
        "current_question": "",
        "candidate_answer": None,
        "score": None,
        "evaluation_reasoning": "",
        "coach_feedback": "",
        "weak_topics": [],
        "round_number": 0,
        "max_rounds": 2,
        "topics_pool": [
            "reciprocal rank fusion", "hybrid retrieval", "KV caching",
            "HNSW", "LangGraph vs CrewAI",
        ],
        "question_context": [],
        "evaluation_context": [],
        "session_log": [],
    }

    result = app.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        interrupt_info = result["__interrupt__"][0].value

        if interrupt_info["type"] == "select_topic":
            print("\nAvailable topics:")
            for i, t in enumerate(interrupt_info["topics_pool"], 1):
                print(f"  {i}. {t}")
            choice = input("Pick a topic number: ")
            chosen = interrupt_info["topics_pool"][int(choice) - 1]
            result = app.invoke(Command(resume=chosen), config=config)

        elif interrupt_info["type"] == "collect_answer":
            print(f"\nQuestion ({interrupt_info['topic']}): {interrupt_info['question']}")
            answer = input("Your answer: ")
            result = app.invoke(Command(resume=answer), config=config)

    print("\n=== SESSION COMPLETE ===")
    print(f"Rounds completed: {len(result.get('session_log', []))}")

    with open("session_log.json", "w") as f:
        json.dump(result.get("session_log", []), f, indent=2)
    print(f"Saved to session_log.json")