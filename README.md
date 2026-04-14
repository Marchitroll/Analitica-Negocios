# Analítica de Negocios - Proyectos Semanales

Repositorio de proyectos de analítica aplicada por semanas. Cada proyecto sigue un flujo reproducible de entrenamiento, guardado de artefactos y consumo desde aplicaciones Streamlit.

## Distribución actual de la raíz

- [README.md](README.md)
- [requirements.txt](requirements.txt)
- [Semana_1_Proyecto_1](Semana_1_Proyecto_1)
- [Semana_1_Proyecto_2](Semana_1_Proyecto_2)
- [Semana_1_Proyecto_3](Semana_1_Proyecto_3)
- [Semana_1_Proyecto_4](Semana_1_Proyecto_4)
- [Semana_2_Proyecto_5](Semana_2_Proyecto_5)

## Objetivo de negocio

- Estandarizar decisiones preliminares de crédito.
- Estimar salarios de forma orientativa para perfiles laborales.
- Ofrecer evaluaciones orientativas de estrés y ansiedad.
- Incorporar un canal FAQ conversacional para atención al público.
- Transformar datos transaccionales en decisiones comerciales con evidencia estadística.

## Proyectos disponibles

### Semana 1 - Proyecto 1: Crédito

- [Semana_1_Proyecto_1/Credito.ipynb](Semana_1_Proyecto_1/Credito.ipynb)
- [Semana_1_Proyecto_1/app_credito_streamlit.py](Semana_1_Proyecto_1/app_credito_streamlit.py)
- [Semana_1_Proyecto_1/model_credito.joblib](Semana_1_Proyecto_1/model_credito.joblib)
- [Semana_1_Proyecto_1/model_credito_metadata.json](Semana_1_Proyecto_1/model_credito_metadata.json)

### Semana 1 - Proyecto 2: Predicción Salarial

- [Semana_1_Proyecto_2/SalarioPredicción.ipynb](Semana_1_Proyecto_2/SalarioPredicción.ipynb)
- [Semana_1_Proyecto_2/app_salario_streamlit.py](Semana_1_Proyecto_2/app_salario_streamlit.py)
- [Semana_1_Proyecto_2/modelo_salario_pipeline.joblib](Semana_1_Proyecto_2/modelo_salario_pipeline.joblib)

### Semana 1 - Proyecto 3: Salud Mental

- [Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb](Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb)
- [Semana_1_Proyecto_3/stress_SVM.ipynb](Semana_1_Proyecto_3/stress_SVM.ipynb)
- [Semana_1_Proyecto_3/app_salud_mental_streamlit.py](Semana_1_Proyecto_3/app_salud_mental_streamlit.py)
- [Semana_1_Proyecto_3/rl_model_ansiedad.joblib](Semana_1_Proyecto_3/rl_model_ansiedad.joblib)
- [Semana_1_Proyecto_3/svm_classifier_stress.joblib](Semana_1_Proyecto_3/svm_classifier_stress.joblib)
- [Semana_1_Proyecto_3/rl_model_ansiedad_metadata.json](Semana_1_Proyecto_3/rl_model_ansiedad_metadata.json)
- [Semana_1_Proyecto_3/svm_classifier_stress_metadata.json](Semana_1_Proyecto_3/svm_classifier_stress_metadata.json)

### Semana 1 - Proyecto 4: Chatbot FAQ Semántico

- [Semana_1_Proyecto_4/creación_chatbot.ipynb](Semana_1_Proyecto_4/creación_chatbot.ipynb): entrenamiento y validación.
- [Semana_1_Proyecto_4/chatbot_utils.py](Semana_1_Proyecto_4/chatbot_utils.py): utilidades de carga, entrenamiento, predicción y persistencia.
- [Semana_1_Proyecto_4/chatbot_faq.json](Semana_1_Proyecto_4/chatbot_faq.json): base FAQ editable.
- [Semana_1_Proyecto_4/chatbot_tfidf_artifacts.joblib](Semana_1_Proyecto_4/chatbot_tfidf_artifacts.joblib): artefacto de inferencia.
- [Semana_1_Proyecto_4/chatbot_tfidf_metadata.json](Semana_1_Proyecto_4/chatbot_tfidf_metadata.json): metadatos del artefacto.
- [Semana_1_Proyecto_4/app_chatbot_streamlit.py](Semana_1_Proyecto_4/app_chatbot_streamlit.py): interfaz conversacional.

### Semana 2 - Proyecto 5: Estrategia de Ventas Data-Driven

- [Semana_2_Proyecto_5/estrategia_ventas_data_driven.ipynb](Semana_2_Proyecto_5/estrategia_ventas_data_driven.ipynb): análisis integral con EDA, inferencia estadística, clustering y recomendaciones.
- [Semana_2_Proyecto_5/Caso_Data_Driven.ipynb](Semana_2_Proyecto_5/Caso_Data_Driven.ipynb): versión base y de referencia del caso.
- [Semana_2_Proyecto_5/ventas_data_driven.csv](Semana_2_Proyecto_5/ventas_data_driven.csv): dataset transaccional del mini proyecto.

## Flujo de trabajo común

1. Preparar datos de entrada para el caso de uso.
2. Entrenar modelo o pipeline en notebook.
3. Validar resultados y guardar artefactos.
4. Consumir artefactos desde app Streamlit.
5. Para casos data driven, ejecutar análisis inferencial y segmentación para respaldar decisiones de negocio.

## Cómo ejecutar

### 1. Crear entorno virtual

```powershell
python -m venv .venv
```

### 2. Activar entorno en PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar apps Streamlit

```powershell
python -m streamlit run Semana_1_Proyecto_1/app_credito_streamlit.py
python -m streamlit run Semana_1_Proyecto_2/app_salario_streamlit.py
python -m streamlit run Semana_1_Proyecto_3/app_salud_mental_streamlit.py
python -m streamlit run Semana_1_Proyecto_4/app_chatbot_streamlit.py
```

### 5. Entrenar y regenerar artefactos del Proyecto 4

1. Ejecutar [Semana_1_Proyecto_4/creación_chatbot.ipynb](Semana_1_Proyecto_4/creación_chatbot.ipynb).
2. Verificar que se actualicen [Semana_1_Proyecto_4/chatbot_tfidf_artifacts.joblib](Semana_1_Proyecto_4/chatbot_tfidf_artifacts.joblib) y [Semana_1_Proyecto_4/chatbot_tfidf_metadata.json](Semana_1_Proyecto_4/chatbot_tfidf_metadata.json).
3. Levantar [Semana_1_Proyecto_4/app_chatbot_streamlit.py](Semana_1_Proyecto_4/app_chatbot_streamlit.py).

### 6. Ejecutar el mini proyecto de estrategia comercial (Proyecto 5)

1. Abrir [Semana_2_Proyecto_5/estrategia_ventas_data_driven.ipynb](Semana_2_Proyecto_5/estrategia_ventas_data_driven.ipynb).
2. Ejecutar las celdas en orden para reproducir EDA, pruebas de hipótesis, segmentación y tablero gerencial.
3. Validar decisiones finales de promociones y bono con base en los p-values reportados.

## Notas

- Las predicciones son orientativas y no sustituyen evaluaciones formales.
- En Proyecto 4, el comportamiento de fallback se activa cuando el score de similitud es menor al threshold configurado.
- La app del Proyecto 4 consume artefactos serializados y metadatos generados por notebook.
- En Proyecto 5, las conclusiones son inferenciales y deben actualizarse periódicamente con datos nuevos.
