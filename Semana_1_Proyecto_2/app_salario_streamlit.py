from pathlib import Path

import joblib
import pandas as pd
import sklearn
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "modelo_salario_pipeline.joblib"
APP_TITLE = "PREDICCIÓN DE SALARIO"

PAISES_TRAD = {
    "Estados Unidos": "United States",
    "India": "India",
    "Reino Unido": "United Kingdom",
    "Alemania": "Germany",
    "Canadá": "Canada",
    "Brasil": "Brazil",
    "Francia": "France",
    "España": "Spain",
    "Australia": "Australia",
    "Países Bajos": "Netherlands",
    "Polonia": "Poland",
    "Italia": "Italy",
    "Federación Rusa": "Russian Federation",
    "Suecia": "Sweden",
}

EDUCACION_TRAD = {
    "Sin licenciatura": "Less than a Bachelors",
    "Licenciatura": "Bachelor's degree",
    "Maestría": "Master's degree",
    "Postgrado": "Post grad",
}


def set_page() -> None:
    st.set_page_config(
        page_title="Predicción de salario",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


@st.cache_resource
def load_resources():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No existe el modelo: {MODEL_PATH}")

    try:
        artifact = joblib.load(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(f"No se pudo cargar el modelo (archivo corrupto o inválido): {exc}") from exc

    required_keys = {"model", "feature_columns", "versions"}
    missing = required_keys.difference(artifact.keys())
    if missing:
        raise ValueError(f"Faltan claves en el artefacto: {sorted(missing)}")

    expected_sklearn = artifact["versions"].get("sklearn")
    if expected_sklearn and expected_sklearn != sklearn.__version__:
        raise RuntimeError(
            "Versión de scikit-learn incompatible. "
            f"Esperada: {expected_sklearn}, actual: {sklearn.__version__}."
        )

    model = artifact["model"]
    return model, artifact


def render_form(feature_columns: list[str]):
    with st.form("salary_form", clear_on_submit=False):
        st.subheader("Características del perfil")
        st.caption("Completa los campos y presiona Predecir.")

        col1, col2, col3 = st.columns(3)

        with col1:
            pais_display = st.selectbox(
                "País",
                options=list(PAISES_TRAD.keys()),
                index=0,
                help="País del perfil a evaluar.",
            )
            pais = PAISES_TRAD.get(pais_display) if pais_display else None

        with col2:
            educacion_display = st.selectbox(
                "Educación",
                options=list(EDUCACION_TRAD.keys()),
                index=0,
                help="Nivel educativo del perfil.",
            )
            educacion = EDUCACION_TRAD.get(educacion_display) if educacion_display else None

        with col3:
            anios_raw = st.text_input(
                "Años de experiencia",
                value="",
                placeholder="Ejemplo: 7",
                help="Ingresa un número mayor o igual a 0.",
            )

        submitted = st.form_submit_button("Predecir")

    if not submitted:
        return None

    missing_inputs = []
    if pais is None:
        missing_inputs.append("País")
    if educacion is None:
        missing_inputs.append("Educación")
    if not anios_raw.strip():
        missing_inputs.append("Años_experiencia")

    if missing_inputs:
        raise ValueError(f"Faltan campos obligatorios: {missing_inputs}")

    try:
        anios_experiencia = float(anios_raw.replace(",", "."))
    except ValueError as exc:
        raise ValueError("Años_experiencia debe ser numérico.") from exc

    if anios_experiencia < 0:
        raise ValueError("Años_experiencia no puede ser negativo.")

    values = {
        "Pais": pais,
        "Educación": educacion,
        "Años_experiencia": anios_experiencia,
    }

    missing_columns = [name for name in feature_columns if name not in values]
    if missing_columns:
        raise ValueError(f"El modelo espera columnas no configuradas en la aplicación: {missing_columns}")

    ordered_values = {name: values[name] for name in feature_columns}
    return pd.DataFrame([ordered_values])


def render_prediction(model, features_df: pd.DataFrame) -> None:
    salary_prediction = float(model.predict(features_df)[0])
    st.metric("Salario estimado (S/)", f"{salary_prediction:,.2f}")
    st.caption("Estimación orientativa del modelo. No reemplaza una evaluación salarial formal.")


def main() -> None:
    set_page()
    st.title(APP_TITLE)

    try:
        model, artifact = load_resources()
    except Exception as exc:
        st.error(f"No fue posible cargar recursos: {exc}")
        st.stop()

    st.sidebar.header("Estado")
    st.sidebar.write(f"Modelo: {MODEL_PATH.name}")
    st.sidebar.write(f"scikit-learn: {sklearn.__version__}")
    st.sidebar.write(f"Creado: {artifact.get('created_at_utc', 'N/D')}")

    feature_columns = artifact["feature_columns"]

    try:
        features_df = render_form(feature_columns)
    except Exception as exc:
        st.error(f"Error en formulario: {exc}")
        st.stop()

    if features_df is None:
        st.caption("Completa el formulario y presiona Predecir.")
        return

    try:
        render_prediction(model, features_df)
    except Exception as exc:
        st.error(f"Error al predecir: {exc}")


if __name__ == "__main__":
    main()
