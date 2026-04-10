from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATHS = {
    "estres": BASE_DIR / "svm_classifier_stress.joblib",
    "ansiedad": BASE_DIR / "rl_model_ansiedad.joblib",
}

SURVEYS = {
    "Estres": {
        "model_key": "estres",
        "title": "Evaluacion del nivel de estres",
        "result_prefix": "NIVEL DE ESTRES",
        "feature_names": ["P_E1", "P_E2", "P_E3", "P_E4", "P_E5", "P_E6"],
        "options": [
            "Nunca",
            "Casi nunca",
            "De vez en cuando",
            "Casi siempre",
            "Siempre",
        ],
        "value_map": {
            "Nunca": 0,
            "Casi nunca": 1,
            "De vez en cuando": 2,
            "Casi siempre": 3,
            "Siempre": 4,
        },
        "label_map": {
            "ESTRES_ALTO": "ALTO",
            "ESTRES_MEDIO": "MEDIO",
            "ESTRES_BAJO": "BAJO",
            "SIN_ESTRES": "SIN ESTRES",
        },
        "questions": [
            "Con que frecuencia ha estado afectado por algo que ha ocurrido inesperadamente?",
            "Con que frecuencia se ha sentido incapaz de controlar las cosas importantes en su vida?",
            "Con que frecuencia se ha sentido nervioso o estresado?",
            "Con que frecuencia ha sentido que no podia afrontar todas las cosas que tenia que hacer?",
            "Con que frecuencia ha estado enfadado porque las cosas que le han ocurrido estaban fuera de su control?",
            "Con que frecuencia ha sentido que las dificultades se acumulan tanto que no puede superarlas?",
        ],
    },
    "Ansiedad": {
        "model_key": "ansiedad",
        "title": "Evaluacion del nivel de ansiedad",
        "result_prefix": "NIVEL DE ANSIEDAD",
        "feature_names": ["P_A1", "P_A2", "P_A3", "P_A4", "P_A5", "P_A6"],
        "options": [
            "Nunca",
            "Varios dias",
            "La mitad de los dias",
            "Casi cada dia",
        ],
        "value_map": {
            "Nunca": 0,
            "Varios dias": 1,
            "La mitad de los dias": 2,
            "Casi cada dia": 3,
        },
        "label_map": {
            "ANSIEDAD GRAVE": "GRAVE",
            "ANSIEDAD MODERADA": "MODERADA",
            "ANSIEDAD LEVE": "LEVE",
            "SIN ANSIEDAD": "SIN ANSIEDAD",
        },
        "questions": [
            "Se siente nervioso, ansioso y/o notar que se le ponen los nervios de punta?",
            "Se preocupa demasiado sobre diferentes cosas?",
            "Tiene dificultad para relajarse?",
            "Se siente tan desasosegado que le resulta dificil parar quieto?",
            "Se siente facilmente disgustado o irritable?",
            "Se siente asustado como si algo horrible pudiese pasar?",
        ],
    },
}


def set_page() -> None:
    st.set_page_config(
        page_title="Encuesta de Salud Mental",
        layout="wide",
        initial_sidebar_state="expanded",
    )


@st.cache_resource(show_spinner="Cargando modelos...")
def load_models():
    missing = [str(path) for path in MODEL_PATHS.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("No se encontraron los modelos: " + ", ".join(missing))

    models = {
        "estres": joblib.load(MODEL_PATHS["estres"]),
        "ansiedad": joblib.load(MODEL_PATHS["ansiedad"]),
    }
    return models


def render_selector() -> str:
    with st.sidebar:
        st.title("Formularios")
        choices = list(SURVEYS.keys())

        if hasattr(st.sidebar, "segmented_control"):
            selected = st.sidebar.segmented_control(
                "Selecciona una encuesta",
                choices,
                default=choices[0],
            )
        else:
            selected = st.sidebar.radio("Selecciona una encuesta", choices, index=0)

        st.divider()
        st.caption("Modelos cargados desde archivos .joblib")
        st.caption(f"Estres: {MODEL_PATHS['estres'].name}")
        st.caption(f"Ansiedad: {MODEL_PATHS['ansiedad'].name}")

    return selected


def run_survey(selected_survey: str, model) -> None:
    cfg = SURVEYS[selected_survey]

    st.header(cfg["title"])
    st.caption("Responde las 6 preguntas y presiona Evaluar.")

    form_key = f"form_{cfg['model_key']}"
    answers = []

    with st.form(form_key, clear_on_submit=False):
        for idx, question in enumerate(cfg["questions"], start=1):
            answer = st.radio(
                label=f"{idx}. {question}",
                options=cfg["options"],
                key=f"{cfg['model_key']}_q{idx}",
            )
            answers.append(answer)

        submitted = st.form_submit_button("Evaluar")

    if not submitted:
        return

    try:
        vector = [cfg["value_map"][answer] for answer in answers]
    except KeyError:
        st.error("Hay respuestas invalidas. Vuelve a intentarlo.")
        return

    data = pd.DataFrame([vector], columns=cfg["feature_names"])

    try:
        prediction = model.predict(data)[0]
    except Exception as exc:
        st.error(f"No fue posible ejecutar la prediccion: {exc}")
        return

    label_map = cfg["label_map"]
    label = label_map.get(str(prediction), label_map.get(prediction, str(prediction)))
    st.success(f"{cfg['result_prefix']}: {label}")


def main() -> None:
    set_page()
    st.title("Encuesta de Salud Mental")

    try:
        models = load_models()
    except Exception as exc:
        st.error(f"No fue posible cargar los modelos: {exc}")
        st.stop()

    selected = render_selector()
    selected_cfg = SURVEYS[selected]
    model = models[selected_cfg["model_key"]]

    run_survey(selected, model)


if __name__ == "__main__":
    main()