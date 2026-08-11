import sys
import os
import json
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from langgraph.types import Command
from pathlib import Path
from src.utils.load_topics import load_topics
from src.graph.session_graph import build_graph
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Interview Coach", page_icon="🎯", layout="centered")


@st.cache_resource
def get_app():
    return build_graph()



PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "questions"

app = get_app()

TOPICS_POOL = load_topics(DATA_DIR)
MAX_ROUNDS = 5


def safe_invoke(payload, config):
    """
    Wraps app.invoke so a crash (LLM error, network issue, malformed agent
    output that slipped past the node-level try/except) shows a friendly
    message with a retry option instead of Streamlit's raw traceback page
    taking down the whole session.
    """
    try:
        return app.invoke(payload, config=config), None
    except Exception as e:
        logger.error(f"Graph invocation failed: {e}")
        return None, str(e)


def start_new_session():
    thread_id = str(uuid.uuid4())
    st.session_state.thread_id = thread_id
    st.session_state.config = {"configurable": {"thread_id": thread_id}}
    st.session_state.history = []

    initial_state = {
        "topic": "",
        "current_question": "",
        "candidate_answer": None,
        "score": None,
        "evaluation_reasoning": "",
        "coach_feedback": "",
        "weak_topics": [],
        "round_number": 0,
        "max_rounds": MAX_ROUNDS,
        "topics_pool": TOPICS_POOL,
        "question_context": [],
        "evaluation_context": [],
        "session_log": [],
    }

    result, error = safe_invoke(initial_state, st.session_state.config)
    st.session_state.result = result
    st.session_state.error = error


if "thread_id" not in st.session_state:
    start_new_session()

result = st.session_state.get("result")
error = st.session_state.get("error")

st.title("🎯 Interview Coach")
st.caption("Agentic RAG interview practice — LangGraph + CrewAI + Qdrant")

with st.sidebar:
    if result:
        st.metric("Round", f"{result.get('round_number', 0)} / {MAX_ROUNDS}")
        if result.get("weak_topics"):
            st.markdown("**Weak topics so far:**")
            for t in result["weak_topics"]:
                st.markdown(f"- {t}")
    if st.button("🔄 Start new session"):
        start_new_session()
        st.rerun()

# ---------- Hard failure: invoke itself raised ----------
if error:
    st.error(f"Something went wrong: {error}")
    st.caption("This is usually a transient API issue (rate limit, network blip). Check interview_coach.log for details.")
    if st.button("Retry"):
        st.session_state.error = None
        st.rerun()
    st.stop()

if result is None:
    st.warning("No active session.")
    st.stop()

for i, round_record in enumerate(st.session_state.history, start=1):
    score_display = round_record["score"] if round_record["score"] is not None else "N/A"
    with st.expander(f"Round {i}: {round_record['topic']} — score {score_display}/5"):
        st.markdown(f"**Q:** {round_record['question']}")
        st.markdown(f"**Your answer:** {round_record['answer']}")
        st.markdown(f"**Evaluation:** {round_record['evaluation_reasoning']}")
        st.markdown(f"**Coach feedback:** {round_record['coach_feedback']}")

is_paused = "__interrupt__" in result

if is_paused:
    interrupt_info = result["__interrupt__"][0].value
    pause_type = interrupt_info.get("type")

    if pause_type == "select_topic":
        st.subheader("Pick a topic")
        topics = interrupt_info["topics_pool"]
        weak = interrupt_info.get("weak_topics", [])
        if weak:
            st.caption(f"⚠️ Weak so far: {', '.join(weak)}")

        chosen = st.radio("Choose your next question's topic:", topics, key=f"topic_pick_{result.get('round_number')}")
        if st.button("Ask me this topic"):
            with st.spinner("Preparing your question..."):
                new_result, new_error = safe_invoke(Command(resume=chosen), st.session_state.config)
            st.session_state.result = new_result
            st.session_state.error = new_error
            st.rerun()

    elif pause_type == "collect_answer":
        st.subheader(f"Question — Topic: {interrupt_info['topic']}")
        st.markdown(interrupt_info["question"])

        with st.form(key=f"answer_form_{result.get('round_number')}"):
            answer = st.text_area("Your answer", height=150)
            submitted = st.form_submit_button("Submit answer")

        if submitted and answer.strip():
            with st.spinner("Evaluating your answer..."):
                new_result, new_error = safe_invoke(Command(resume=answer), st.session_state.config)

            if new_result and new_result.get("session_log"):
                st.session_state.history.append(new_result["session_log"][-1])

            st.session_state.result = new_result
            st.session_state.error = new_error
            st.rerun()

    else:
        st.error(f"Unknown pause type: {pause_type!r} — this shouldn't happen. Check interview_coach.log.")

else:
    st.success("Session complete! 🎉")
    st.subheader("Summary")
    # Filter out None scores (rounds where the Evaluator agent failed) so
    # the average isn't computed over a mix of ints and Nones.
    scores = [r["score"] for r in st.session_state.history if r["score"] is not None]
    unscored = len(st.session_state.history) - len(scores)
    if scores:
        st.metric("Average score", f"{sum(scores) / len(scores):.1f} / 5")
    if unscored:
        st.caption(f"⚠️ {unscored} round(s) couldn't be scored due to an evaluator error.")

    with open("session_log.json", "w") as f:
        json.dump(result.get("session_log", []), f, indent=2)
    st.caption("Session log saved to session_log.json for RAGAS evaluation.")

    if st.button("Start another session"):
        start_new_session()
        st.rerun()
        