import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_THRESHOLD = 0.30

SPANISH_STOPWORDS = [
    "a",
    "al",
    "con",
    "como",
    "cual",
    "cuales",
    "de",
    "del",
    "donde",
    "el",
    "en",
    "es",
    "esta",
    "la",
    "las",
    "lo",
    "los",
    "me",
    "mi",
    "mis",
    "necesito",
    "para",
    "por",
    "puedo",
    "que",
    "quiero",
    "se",
    "su",
    "sus",
    "un",
    "una",
    "y",
]


def load_faq(faq_path: Path) -> list[dict[str, Any]]:
    if not faq_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo FAQ: {faq_path}")

    with faq_path.open("r", encoding="utf-8") as fh:
        faq_items = json.load(fh)

    if not isinstance(faq_items, list) or not faq_items:
        raise ValueError("El archivo FAQ debe contener una lista con elementos.")

    required_keys = {"id", "answer", "questions"}
    for index, item in enumerate(faq_items):
        if not isinstance(item, dict):
            raise ValueError(f"El item {index} no es un objeto JSON valido.")

        missing = required_keys - set(item.keys())
        if missing:
            raise ValueError(f"El item {index} no incluye llaves requeridas: {sorted(missing)}")

        if not isinstance(item["questions"], list) or not item["questions"]:
            raise ValueError(f"El item {index} debe incluir una lista de preguntas no vacia.")

    return faq_items


def _build_training_rows(faq_items: list[dict[str, Any]]) -> tuple[list[str], list[dict[str, Any]]]:
    training_questions: list[str] = []
    answer_lookup: list[dict[str, Any]] = []

    for item in faq_items:
        canonical_question = item["questions"][0]
        for question in item["questions"]:
            training_questions.append(question)
            answer_lookup.append(
                {
                    "id": item["id"],
                    "category": item.get("category", "general"),
                    "canonical_question": canonical_question,
                    "question": question,
                    "answer": item["answer"],
                }
            )

    return training_questions, answer_lookup


def train_artifacts(faq_path: Path, threshold: float = DEFAULT_THRESHOLD) -> dict[str, Any]:
    threshold_value = float(threshold)
    if not 0.0 <= threshold_value <= 1.0:
        raise ValueError("El threshold debe estar entre 0 y 1.")

    faq_items = load_faq(faq_path)
    training_questions, answer_lookup = _build_training_rows(faq_items)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        stop_words=SPANISH_STOPWORDS,
        min_df=1,
        sublinear_tf=True,
    )
    question_matrix = vectorizer.fit_transform(training_questions)

    return {
        "vectorizer": vectorizer,
        "question_matrix": question_matrix,
        "answer_lookup": answer_lookup,
        "threshold": threshold_value,
        "faq_file": faq_path.name,
    }


def _build_suggestions(similarities: Any, answer_lookup: list[dict[str, Any]], top_n: int = 3) -> list[str]:
    if similarities.size == 0:
        return []

    ranked_indices = similarities.argsort()[::-1]
    suggestions: list[str] = []

    for index in ranked_indices:
        canonical = answer_lookup[int(index)]["canonical_question"]
        if canonical not in suggestions:
            suggestions.append(canonical)
        if len(suggestions) == top_n:
            break

    return suggestions


def predict_response(
    user_input: str,
    artifact: dict[str, Any],
) -> dict[str, Any]:
    question = user_input.strip()
    if not question:
        return {
            "status": "fallback",
            "score": 0.0,
            "answer": "Por favor escribe una consulta para poder ayudarte.",
            "matched_question": None,
            "category": None,
            "suggestions": [],
            "handoff_recommended": False,
        }

    vectorizer = artifact["vectorizer"]
    question_matrix = artifact["question_matrix"]
    answer_lookup = artifact["answer_lookup"]
    threshold = float(artifact.get("threshold", DEFAULT_THRESHOLD))

    query_vector = vectorizer.transform([question])
    similarities = cosine_similarity(query_vector, question_matrix).ravel()

    if similarities.size == 0:
        return {
            "status": "fallback",
            "score": 0.0,
            "answer": "No tengo datos suficientes para responder esa consulta.",
            "matched_question": None,
            "category": None,
            "suggestions": [],
            "handoff_recommended": True,
        }

    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])
    best_match = answer_lookup[best_index]

    if best_score >= threshold:
        return {
            "status": "match",
            "score": best_score,
            "answer": best_match["answer"],
            "matched_question": best_match["question"],
            "category": best_match["category"],
            "suggestions": [],
            "handoff_recommended": False,
        }

    suggestions = _build_suggestions(similarities, answer_lookup, top_n=3)
    fallback_message = (
        "No estoy totalmente seguro de tu consulta. "
        "Puedes reformular la pregunta o pedir hablar con un asesor humano."
    )

    return {
        "status": "fallback",
        "score": best_score,
        "answer": fallback_message,
        "matched_question": best_match["question"],
        "category": best_match["category"],
        "suggestions": suggestions,
        "handoff_recommended": True,
    }


def save_artifacts(
    artifact_path: Path,
    metadata_path: Path,
    artifact: dict[str, Any],
    faq_items: list[dict[str, Any]],
) -> dict[str, Any]:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(artifact, artifact_path)

    metadata = {
        "artifact_file": artifact_path.name,
        "faq_file": artifact.get("faq_file", ""),
        "threshold": float(artifact.get("threshold", DEFAULT_THRESHOLD)),
        "faq_entries": len(faq_items),
        "training_questions": len(artifact["answer_lookup"]),
        "vectorizer": {
            "class": artifact["vectorizer"].__class__.__name__,
            "ngram_range": list(artifact["vectorizer"].ngram_range),
            "vocabulary_size": int(len(artifact["vectorizer"].vocabulary_)),
        },
        "library_versions": {
            "scikit_learn": sklearn.__version__,
            "joblib": joblib.__version__,
        },
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    with metadata_path.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, ensure_ascii=False, indent=2)

    return metadata


def load_artifacts(artifact_path: Path) -> dict[str, Any]:
    if not artifact_path.exists():
        raise FileNotFoundError(f"No se encontro el artefacto del modelo: {artifact_path}")
    return joblib.load(artifact_path)
