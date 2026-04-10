# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 18:53:24 2023

@author: ALDO MEZA 
"""

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

with st.sidebar:
    selected = option_menu(
        menu_title="Formularios",
        options=["Ansiedad", "Estrés"],
        icons=["heart-pulse", "heart-pulse-fill"],
        menu_icon="pencil-square"
    )

model_stress = pickle.load(open('svm_classifier_stress.pkl', 'rb'))

items_estres = ['Nunca', 'Casi nunca', 'De vez en cuando', 'Casi siempre', 'Siempre']

values1 = {'Nunca': 0, 'Casi nunca': 1, 'De vez en cuando': 2, 'Casi siempre': 3, 'Siempre': 4}

labels_estres = {'ESTRES_ALTO': 'ALTO',
                 'ESTRES_MEDIO': 'MEDIO',
                 'ESTRES_BAJO': 'BAJO',
                 'SIN_ESTRES': 'SIN ESTRÉS'}

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


model_anxiety = pickle.load(open('rl_model_ansiedad.pkl', 'rb'))

items_ansiedad = ['Nunca', 'Varios días', 'La mitad de los días', 'Casi cada día']

values2 = {'Nunca': 0, 'Varios días': 1, 'La mitad de los días': 2, 'Casi cada día': 3}

labels_anxiety = {'ANSIEDAD GRAVE': 'GRAVE',
                  'ANSIEDAD MODERADA': 'MODERADA',
                  'ANSIEDAD LEVE': 'LEVE',
                  'SIN ANSIEDAD': 'SIN ANSIEDAD'}
    
if selected == "Ansiedad":
    st.header('Evaluación del nivel de ansiedad')
    ansied_q1 = st.radio( label="1. ¿Se siente nervioso, ansioso y/o notar que se le ponen los nervios de punta?",
                          options=items_ansiedad)
    ansied_q2 = st.radio(label="2. ¿Se preocupa demasiado sobre diferentes cosas?",
                         options=items_ansiedad)
    ansied_q3 = st.radio(label="3. ¿Tiene dificultad para relajarse?",
                         options=items_ansiedad)
    ansied_q4 = st.radio(label="4. ¿Se siente tan desasosegado que le resulta difícil parar quieto?",
                         options=items_ansiedad)
    ansied_q5 = st.radio(label="5. ¿Se siente fácilmente disgustado o irritable?",
                         options=items_ansiedad)
    ansied_q6 = st.radio(label="6. ¿Se siente asustado como si algo horrible pudiese pasar?",
                         options=items_ansiedad)

    if st.button("Evaluar"):
        data1_X = []
        data1_X.append(values2.get(ansied_q1))
        data1_X.append(values2.get(ansied_q2))
        data1_X.append(values2.get(ansied_q3))
        data1_X.append(values2.get(ansied_q4))
        data1_X.append(values2.get(ansied_q5))
        data1_X.append(values2.get(ansied_q6))

        data_evaluate1 = np.array([data1_X])
        pred1 = model_anxiety.predict(data_evaluate1)
        st.success('NIVEL DE ANSIEDAD: {}'.format(labels_anxiety.get(pred1[0]))) 