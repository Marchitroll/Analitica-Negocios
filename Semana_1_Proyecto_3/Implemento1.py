from streamlit_option_menu import option_menu
import streamlit as st
import numpy as np
import pickle

st.set_page_config(
    page_title="Encuesta de Salud Mental",
    #page_icon="./images/logo-naal.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

model_stress = pickle.load(open('svm_classifier_stress.pkl', 'rb'))

with st.sidebar:
    selected = option_menu(
        menu_title="Formulario",
        options=["Estrés"],
        icons=["heart-pulse-fill"],
        menu_icon="pencil-square"
    )

items_estres = ['Nunca', 'Casi nunca', 'De vez en cuando', 'Casi siempre', 'Siempre']

if selected == "Estrés":
    st.header('Evaluación del nivel de estrés')
    estres_q1 = st.radio( label="1. ¿Con qué frecuencia ha estado afectado por algo que ha ocurrido inesperadamente?",
                          options=items_estres)
    estres_q2 = st.radio(label="2. ¿Con qué frecuencia se ha sentido incapaz de controlar las cosas importantes en su vida?",
                         options=items_estres)
    estres_q3 = st.radio(label="3. ¿Con qué frecuencia se ha sentido nervioso o estresado?",
                         options=items_estres)
    estres_q4 = st.radio(label="4. ¿Con qué frecuencia ha sentido que no podía afrontar todas las cosas que tenía que hacer?",
                         options=items_estres)
    estres_q5 = st.radio(label="5. ¿Con qué frecuencia ha estado enfadado porque las cosas que le han ocurrido estaban fuera de su control?",
                         options=items_estres)
    estres_q6 = st.radio(label="6. ¿Con qué frecuencia ha sentido que las dificultades se acumulan tanto que no puede superarlas?",
                         options=items_estres)



values1 = {'Nunca': 0, 'Casi nunca': 1, 'De vez en cuando': 2, 'Casi siempre': 3, 'Siempre': 4}

labels_estres = {'ESTRES_ALTO': 'ALTO',
                 'ESTRES_MEDIO': 'MEDIO',
                 'ESTRES_BAJO': 'BAJO',
                 'SIN_ESTRES': 'SIN ESTRÉS'}

if st.button("Evaluar"):
    data_X = []
    data_X.append(values1.get(estres_q1))
    data_X.append(values1.get(estres_q2))
    data_X.append(values1.get(estres_q3))
    data_X.append(values1.get(estres_q4))
    data_X.append(values1.get(estres_q5))
    data_X.append(values1.get(estres_q6))

    data_evaluate = np.array([data_X])
    pred = model_stress.predict(data_evaluate)
    st.success('NIVEL DE ESTRÉS: {}'.format(labels_estres.get(pred[0])))

