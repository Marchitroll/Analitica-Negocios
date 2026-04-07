from pathlib import Path
import json

# Ejecutar desde la raiz del repositorio:
# python -m streamlit run Semana_1_Proyecto_1/app_credito_streamlit.py

import joblib
import pandas as pd
import sklearn
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model_credito.joblib"
METADATA_PATH = BASE_DIR / "model_credito_metadata.json"
APP_TITLE = "EVALUACION DE CREDITO"

FIELD_SPECS = [
    {
        "name": "Edad",
        "label": "Edad (años)",
        "help": "Edad del solicitante en años cumplidos.",
        "min_value": 18,
        "max_value": 100,
        "value": 35,
        "step": 1,
        "format": "%d",
        "icon": ":material/person:",
    },
    {
        "name": "Tarjetas",
        "label": "Tarjetas activas",
        "help": "Cantidad de tarjetas de crédito activas.",
        "min_value": 0,
        "max_value": 20,
        "value": 1,
        "step": 1,
        "format": "%d",
        "icon": ":material/credit_card:",
    },
    {
        "name": "Deuda",
        "label": "Deuda total (S/)",
        "help": "Saldo total adeudado por el cliente.",
        "min_value": 0.0,
        "max_value": None,
        "value": 1000.0,
        "step": 100.0,
        "format": "%.2f",
        "icon": ":material/payments:",
    },
    {
        "name": "Saldo",
        "label": "Saldo disponible (S/)",
        "help": "Saldo actual reportado por el cliente.",
        "min_value": 0.0,
        "max_value": None,
        "value": 0.0,
        "step": 100.0,
        "format": "%.2f",
        "icon": ":material/account_balance_wallet:",
    },
    {
        "name": "CrediScore",
        "label": "Score crediticio (0 a 10)",
        "help": "Puntaje financiero normalizado en escala de 0 a 10.",
        "min_value": 0.0,
        "max_value": 10.0,
        "value": 5.0,
        "step": 0.1,
        "format": "%.1f",
        "icon": ":material/finance:",
    },
    {
        "name": "Años_empleo",
        "label": "Años de empleo",
        "help": "Antigüedad laboral del solicitante.",
        "min_value": 0,
        "max_value": 60,
        "value": 3,
        "step": 1,
        "format": "%d",
        "icon": ":material/work:",
    },
    {
        "name": "Ingresos",
        "label": "Ingresos mensuales (S/)",
        "help": "Ingreso mensual aproximado del solicitante.",
        "min_value": 0.0,
        "max_value": None,
        "value": 2000.0,
        "step": 100.0,
        "format": "%.2f",
        "icon": ":material/payments:",
    },
]

FIELD_SPEC_BY_NAME = {spec["name"]: spec for spec in FIELD_SPECS}

def set_page() -> None:
    st.set_page_config(
        page_title="Solicitud para aprobacion de credito",
        page_icon="credito.png",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


@st.cache_resource
def load_resources():
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"No existe metadata: {METADATA_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No existe modelo: {MODEL_PATH}")

    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    required_keys = {"feature_columns", "label_mapping", "library_versions"}
    missing = required_keys.difference(metadata.keys())
    if missing:
        raise ValueError(f"Faltan claves en metadata: {sorted(missing)}")

    expected_sklearn = metadata["library_versions"].get("scikit_learn")
    if expected_sklearn and expected_sklearn != sklearn.__version__:
        raise RuntimeError(
            "Version de scikit-learn incompatible. "
            f"Esperada: {expected_sklearn}, actual: {sklearn.__version__}."
        )

    model = joblib.load(MODEL_PATH)
    return model, metadata


def render_number_input(spec: dict) -> float:
    input_kwargs = {
        "label": spec["label"],
        "min_value": spec["min_value"],
        "value": spec["value"],
        "step": spec["step"],
        "format": spec["format"],
        "help": spec["help"],
        "icon": spec["icon"],
    }
    max_value = spec.get("max_value")
    if max_value is not None:
        input_kwargs["max_value"] = max_value

    return st.number_input(**input_kwargs)


def render_form(feature_columns):
    with st.form("credit_form", clear_on_submit=False):
        st.subheader("Caracteristicas del cliente")
        st.caption("Los campos enteros se muestran como enteros; los monetarios usan separador de miles y dos decimales, expresados en soles.")

        left_col, right_col = st.columns(2)
        values = {}

        with left_col:
            st.markdown("**Perfil general**")
            for spec in FIELD_SPECS[:3]:
                values[spec["name"]] = render_number_input(spec)

        with right_col:
            st.markdown("**Finanzas y estabilidad**")
            for spec in FIELD_SPECS[3:]:
                values[spec["name"]] = render_number_input(spec)

        submitted = st.form_submit_button("Predecir")

    if not submitted:
        return None

    missing_inputs = [name for name in feature_columns if name not in values]
    if missing_inputs:
        raise ValueError(f"No se capturaron todas las variables: {missing_inputs}")

    ordered_values = {name: values[name] for name in feature_columns}
    return pd.DataFrame([ordered_values])


def render_prediction(model, metadata, features_df: pd.DataFrame) -> None:
    pred = int(model.predict(features_df)[0])

    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(features_df)[0, 1])

    label_map = metadata.get("label_mapping", {})
    decision = label_map.get(str(pred), str(pred))

    result_col, proba_col = st.columns(2)
    with result_col:
        st.metric("Decisión", decision)
    with proba_col:
        if proba is not None:
            st.metric("Probabilidad de aprobación", f"{proba:.1%}")
            st.progress(proba)

    st.caption("Resultado orientativo. No reemplaza la evaluacion crediticia formal.")


def main() -> None:
    set_page()
    st.title(APP_TITLE)

    try:
        model, metadata = load_resources()
    except Exception as exc:
        st.error(f"No fue posible cargar recursos: {exc}")
        st.stop()

    st.sidebar.header("Estado")
    st.sidebar.write(f"Modelo: {MODEL_PATH.name}")
    st.sidebar.write(f"scikit-learn: {sklearn.__version__}")
    st.sidebar.divider()
    st.sidebar.markdown("**Guía rápida**")
    st.sidebar.caption("Completa el formulario, revisa los valores formateados en soles y presiona Predecir.")

    feature_columns = metadata["feature_columns"]

    if feature_columns != [spec["name"] for spec in FIELD_SPECS]:
        st.error("La configuración visual no coincide con el orden esperado por el modelo.")
        st.stop()

    try:
        features_df = render_form(feature_columns)
    except Exception as exc:
        st.error(f"Error en formulario: {exc}")
        st.stop()

    if features_df is None:
        st.caption("Completa el formulario y presiona Predecir.")
        return

    try:
        render_prediction(model, metadata, features_df)
    except Exception as exc:
        st.error(f"Error al predecir: {exc}")


if __name__ == "__main__":
    main()