# -*- coding: utf-8 -*-
"""Aplicación Streamlit para evaluación de salud mental (ansiedad y estrés).

Estructura modular que separa interfaz, evaluación clínica y modelos de
inteligencia artificial. Esta edición refactoriza únicamente los
comentarios y la documentación para mejorar claridad y consistencia;
no modifica la lógica funcional.
"""

from pathlib import Path

import joblib
import numpy as np
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

def set_page() -> None:
    st.set_page_config(
        page_title="Evaluación de Salud Mental",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_styles() -> None:
    st.markdown("""
<style>
    /* Inyectar Google Font Outfit */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Fondo con gradiente sutil y elegante en modo oscuro */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161a24 100%);
        color: #f0f2f6;
    }
    
    /* Estilos para el título principal */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #9ca3af;
        margin-bottom: 2.5rem;
    }
    
    /* Tarjetas premium con efecto Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Estilo para los botones */
    .stButton>button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
    }
    
    /* Radio buttons mejorados */
    div[row-widget="radio"] > div {
        background-color: rgba(255, 255, 255, 0.02);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Alertas de Streamlit personalizadas */
    div.stAlert {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(255, 255, 255, 0.04);
    }
</style>
""", unsafe_allow_html=True)

# Configuración centralizada de cuestionarios (evita duplicación)
# Define preguntas, opciones, reglas clínicas y rutas a modelos por cuestionario
CONFIG = {
    'Ansiedad': {
        'icon': 'heart-pulse',
        'title': 'Evaluación del Nivel de Ansiedad',
        'desc': 'Este cuestionario está basado en la escala estándar de ansiedad (GAD adaptada). Responde con total honestidad.',
        'questions': [
            "1. ¿Se siente nervioso, ansioso y/o notar que se le ponen los nervios de punta?",
            "2. ¿Se preocupa demasiado sobre diferentes cosas?",
            "3. ¿Tiene dificultad para relajarse?",
            "4. ¿Se siente tan desasosegado que le resulta difícil parar quieto?",
            "5. ¿Se siente fácilmente disgustado o irritable?",
            "6. ¿Se siente asustado como si algo horrible pudiese pasar?"
        ],
        'options': ['Nunca', 'Varios días', 'La mitad de los días', 'Casi cada día'],
        'values': {'Nunca': 0, 'Varios días': 1, 'La mitad de los días': 2, 'Casi cada día': 3},
        'clinical_eval': lambda suma: (
            'SIN ANSIEDAD' if suma <= 3 else
            'ANSIEDAD LEVE' if suma <= 8 else
            'ANSIEDAD MODERADA' if suma <= 12 else
            'ANSIEDAD GRAVE'
        ),
        'display_labels': {
            'SIN ANSIEDAD': 'SIN ANSIEDAD',
            'ANSIEDAD LEVE': 'LEVE',
            'ANSIEDAD MODERADA': 'MODERADA',
            'ANSIEDAD GRAVE': 'GRAVE'
        },
        'model_file': BASE_DIR / 'rl_model_ansiedad.joblib'
    },
    'Estrés': {
        'icon': 'heart-pulse-fill',
        'title': 'Evaluación del Nivel de Estrés',
        'desc': 'Este cuestionario está basado en la Escala de Estrés Percibido (PSS adaptada). Responde según tu vivencia del último mes.',
        'questions': [
            "1. ¿Con qué frecuencia ha estado afectado por algo que ha ocurrido inesperadamente?",
            "2. ¿Con qué frecuencia se ha sentido incapaz de controlar las cosas importantes en su vida?",
            "3. ¿Con qué frecuencia se ha sentido nervioso o estresado?",
            "4. ¿Con qué frecuencia ha sentido que no podía afrontar todas las cosas que tenía que hacer?",
            "5. ¿Con qué frecuencia ha estado enfadado porque las cosas que le han ocurrido estaban fuera de su control?",
            "6. ¿Con qué frecuencia ha sentido que las dificultades se acumulan tanto que no puede superarlas?"
        ],
        'options': ['Nunca', 'Casi nunca', 'De vez en cuando', 'Casi siempre', 'Siempre'],
        'values': {'Nunca': 0, 'Casi nunca': 1, 'De vez en cuando': 2, 'Casi siempre': 3, 'Siempre': 4},
        'clinical_eval': lambda suma: (
            'SIN_ESTRES' if suma <= 4 else
            'ESTRES_BAJO' if suma <= 10 else
            'ESTRES_MEDIO' if suma <= 17 else
            'ESTRES_ALTO'
        ),
        'display_labels': {
            'SIN_ESTRES': 'SIN ESTRÉS',
            'ESTRES_BAJO': 'BAJO',
            'ESTRES_MEDIO': 'MEDIO',
            'ESTRES_ALTO': 'ALTO'
        },
        'model_file': BASE_DIR / 'svm_classifier_stress.joblib'
    }
}

@st.cache_resource
def load_models():
    models = {}
    missing = {}
    for key, cfg in CONFIG.items():
        model_path = cfg["model_file"]
        if model_path.exists():
            models[key] = joblib.load(model_path)
        else:
            missing[key] = model_path
    return models, missing


def render_sidebar():
    with st.sidebar:
        st.markdown("<h3 style='text-align: center; color: #10b981; font-weight: 800;'>MENÚ</h3>", unsafe_allow_html=True)

        selected = st.radio(
            label="Formularios",
            options=list(CONFIG.keys()),
            index=0
        )

        st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color: #3b82f6; font-weight: 600;'>Motor de Predicción</h4>", unsafe_allow_html=True)
        prediction_engine = st.radio(
            label="Seleccione el método de evaluación:",
            options=["Motor Clínico (Reglas exactas)", "Motor de Inteligencia Artificial (Modelo ML)"],
            index=0,
            help="El Motor Clínico aplica la suma estandarizada y directa de puntuaciones. El Motor de IA utiliza modelos entrenados en bases de datos con scikit-learn (SVM y Regresión Logística)."
        )

    return selected, prediction_engine

def render_questions(cfg, selected):
    st.markdown(
        f"<div class='glass-card'><h3>{cfg['title']}</h3><p style='color: #9ca3af;'>{cfg['desc']}</p></div>",
        unsafe_allow_html=True
    )

    user_responses = []
    for i, question_text in enumerate(cfg['questions']):
        ans = st.radio(
            label=question_text,
            options=cfg['options'],
            key=f"{selected}_q{i}"
        )
        user_responses.append(cfg['values'][ans])

    return user_responses


def render_results(cfg, selected, prediction_engine, user_responses, models, missing):
    st.markdown("---")
    score_sum = sum(user_responses)

    st.markdown(
        "<h3 style='text-align: center; font-weight: 600;'>RESULTADO DE EVALUACIÓN</h3>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #10b981; margin-top:0;'>Detalle de Puntuación</h4>
            <p style='font-size: 1.2rem; margin-bottom: 0.5rem;'>Puntos Totales Obtenidos: <strong>{score_sum}</strong></p>
            <p style='font-size: 0.95rem; color: #9ca3af;'>Rango de respuestas: 0 a {len(cfg['questions']) * (len(cfg['options']) - 1)} puntos.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if prediction_engine == "Motor Clínico (Reglas exactas)":
            clinical_pred = cfg['clinical_eval'](score_sum)
            display_text = cfg['display_labels'].get(clinical_pred, clinical_pred)

            st.markdown(f"""
            <div class='glass-card' style='border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.02);'>
                <h4 style='color: #3b82f6; margin-top:0;'>Evaluación Clínica (Determinista)</h4>
                <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>Método: Suma acumulada directa</p>
                <div style='font-size: 2rem; font-weight: 800; color: #10b981;'>{display_text}</div>
            </div>
            """, unsafe_allow_html=True)
            return

        model = models.get(selected)
        missing_path = missing.get(selected)

        if missing_path:
            st.markdown(f"""
            <div class='glass-card' style='border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.02);'>
                <h4 style='color: #ef4444; margin-top:0;'>Modelo No Encontrado</h4>
                <p>El archivo de modelo <strong>'{missing_path.name}'</strong> no está disponible.</p>
                <p style='font-size: 0.9rem; color: #9ca3af;'>Por favor, abre y ejecuta todas las celdas del Jupyter Notebook <code>entrenamiento_modelos.ipynb</code> primero para entrenar y guardar los modelos optimizados (formato .joblib).</p>
            </div>
            """, unsafe_allow_html=True)
            return

        if model is None:
            st.error("No se encontró un modelo cargado para este cuestionario.")
            return

        try:
            features = np.array([user_responses])
            pred_class = model.predict(features)[0]
            display_text = cfg['display_labels'].get(pred_class, pred_class)

            prob_desc = ""
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(features)[0]
                max_prob = max(proba) * 100
                prob_desc = f"<p style='font-size: 0.95rem; color: #9ca3af;'>Confianza del modelo: <strong>{max_prob:.1f}%</strong></p>"

            st.markdown(f"""
            <div class='glass-card' style='border-color: rgba(59, 130, 246, 0.4); background: rgba(59, 130, 246, 0.02);'>
                <h4 style='color: #3b82f6; margin-top:0;'>Evaluación por Inteligencia Artificial</h4>
                <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>Modelo: {model.named_steps['classifier'].__class__.__name__}</p>
                <div style='font-size: 2rem; font-weight: 800; color: #3b82f6;'>{display_text}</div>
                {prob_desc}
            </div>
            """, unsafe_allow_html=True)

        except Exception as exc:
            st.error(f"Error al ejecutar el modelo de Inteligencia Artificial: {str(exc)}")


def main() -> None:
    set_page()
    apply_styles()

    selected, prediction_engine = render_sidebar()
    cfg = CONFIG[selected]

    st.markdown("<div class='main-title'>Salud Mental & Bienestar</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Evaluación instantánea del bienestar psicológico mediante herramientas inteligentes</div>",
        unsafe_allow_html=True
    )

    models, missing = load_models()
    user_responses = render_questions(cfg, selected)

    st.write("")

    if st.button("Evaluar Resultados"):
        render_results(cfg, selected, prediction_engine, user_responses, models, missing)

    st.info("ℹ️ **Nota de Descargo**: Esta es una herramienta digital de auto-reporte y orientación educativa. No sustituye un diagnóstico psicológico o psiquiátrico profesional. Si experimentas dificultades persistentes, te animamos a acudir con un profesional de la salud mental.")


if __name__ == "__main__":
    main()
