import json
from pathlib import Path
from typing import Any

import streamlit as st

from chatbot_utils import load_artifacts, predict_response

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_PATH = BASE_DIR / "chatbot_tfidf_artifacts.joblib"
METADATA_PATH = BASE_DIR / "chatbot_tfidf_metadata.json"

CHAT_HISTORY_KEY = "chat_history"
SHOW_SCORE_KEY = "show_score"

st.set_page_config(page_title="Chatbot FAQ", page_icon="💬", layout="centered")
st.title("Asistente de Atencion al Publico")
st.caption("Motor FAQ con TF-IDF, umbral de confianza y fallback guiado.")


@st.cache_resource
def get_artifacts(path: Path, mtime_ns: int) -> dict[str, Any]:
    del mtime_ns
    return load_artifacts(path)


@st.cache_data
def get_metadata(path: Path, mtime_ns: int) -> dict[str, Any]:
    del mtime_ns
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _file_mtime_ns(path: Path) -> int:
    return path.stat().st_mtime_ns if path.exists() else -1


def _init_state() -> None:
    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []
    if SHOW_SCORE_KEY not in st.session_state:
        st.session_state[SHOW_SCORE_KEY] = True


def _clear_history() -> None:
    st.session_state[CHAT_HISTORY_KEY] = []


def _build_extra_text(response: dict[str, Any], show_score: bool) -> str:
    extra_lines: list[str] = []

    if response["status"] == "fallback" and response["suggestions"]:
        suggestions = "\n".join(f"- {item}" for item in response["suggestions"])
        extra_lines.append("Puedes probar con:\n" + suggestions)

    if response["handoff_recommended"]:
        extra_lines.append("Si lo prefieres, escribe: Quiero hablar con un asesor humano")

    if show_score:
        extra_lines.append(f"Score de similitud: {response['score']:.3f}")

    return "\n\n".join(extra_lines)


def _append_turns(user_input: str, artifacts: dict[str, Any]) -> None:
    st.session_state[CHAT_HISTORY_KEY].append({"role": "user", "text": user_input})

    response = predict_response(user_input, artifacts)
    st.session_state[CHAT_HISTORY_KEY].append(
        {
            "role": "assistant",
            "text": response["answer"],
            "extra": _build_extra_text(response, show_score=st.session_state[SHOW_SCORE_KEY]),
        }
    )


def _render_sidebar(metadata: dict[str, Any]) -> None:
    with st.sidebar:
        st.session_state[SHOW_SCORE_KEY] = st.toggle(
            "Mostrar score de confianza",
            value=st.session_state[SHOW_SCORE_KEY],
        )
        st.button("Limpiar conversacion", on_click=_clear_history, use_container_width=True)

        st.subheader("Modelo")
        if metadata:
            st.write(f"Threshold: {metadata.get('threshold', 'n/d')}")
            st.write(f"FAQ entries: {metadata.get('faq_entries', 'n/d')}")
            st.write(f"Preguntas indexadas: {metadata.get('training_questions', 'n/d')}")
            st.write(f"Vocabulario: {metadata.get('vectorizer', {}).get('vocabulary_size', 'n/d')}")
        else:
            st.info("Aun no hay metadata disponible. Ejecuta el notebook de entrenamiento.")


_init_state()

metadata: dict[str, Any] = {}
if METADATA_PATH.exists():
    metadata = get_metadata(METADATA_PATH, _file_mtime_ns(METADATA_PATH))

_render_sidebar(metadata)

if not ARTIFACT_PATH.exists():
    st.error(
        "No se encontro el artefacto del chatbot. Ejecuta el notebook de entrenamiento para generar: "
        f"{ARTIFACT_PATH.name}"
    )
    st.stop()

artifacts = get_artifacts(ARTIFACT_PATH, _file_mtime_ns(ARTIFACT_PATH))

chat_container = st.container()
user_input = st.chat_input("Escribe tu pregunta...")

if user_input:
    _append_turns(user_input, artifacts)

with chat_container:
    for turn in st.session_state[CHAT_HISTORY_KEY]:
        with st.chat_message(turn["role"]):
            st.markdown(turn["text"])
            if turn.get("extra"):
                st.markdown(turn["extra"])
