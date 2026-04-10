# Analitica de Negocios - Proyectos Semanales

Este repositorio reúne proyectos de analitica de negocios que evolucionan por semanas y pueden cubrir multiples areas de negocio, no necesariamente relacionadas entre si.

La idea central es transformar datos en decisiones o estimaciones con un flujo reproducible de entrenamiento y una interfaz ligera para consumo final. A medida que avancen las semanas, este README se ampliara para reflejar los nuevos casos de uso, modelos y aplicaciones.

## Objetivo de negocio

Los objetivos generales son:

- Ayudar a una entidad financiera a tomar decisiones preliminares de credito con mayor consistencia.
- Estimar rangos salariales de forma orientativa para apoyar analisis de perfiles.
- Ofrecer una evaluacion orientativa de estres y ansiedad a partir de cuestionarios breves.
- Documentar y desplegar nuevos casos de analitica de negocios conforme se sumen proyectos semanales.

## Enfoque analitico

Los proyectos se estructuraron con buenas practicas de analitica predictiva:

- Separacion clara entre entrenamiento y despliegue.
- Preprocesamiento dentro de un pipeline para evitar fuga de informacion.
- Validacion con metricas alineadas al tipo de problema (clasificacion o regresion).
- Seleccion del mejor modelo con criterio objetivo por validacion cruzada.
- Persistencia de artefactos para asegurar consistencia entre entrenamiento e inferencia.

## Componentes del proyecto

- [Semana_1_Proyecto_1/Credito.ipynb](Semana_1_Proyecto_1/Credito.ipynb): notebook de entrenamiento, evaluacion y guardado del modelo de credito.
- [Semana_1_Proyecto_1/app_credito_streamlit.py](Semana_1_Proyecto_1/app_credito_streamlit.py): aplicacion Streamlit para evaluar aprobacion de credito.
- [Semana_1_Proyecto_1/model_credito.joblib](Semana_1_Proyecto_1/model_credito.joblib): modelo de credito entrenado listo para inferencia.
- [Semana_1_Proyecto_1/model_credito_metadata.json](Semana_1_Proyecto_1/model_credito_metadata.json): metadata de despliegue del modelo de credito.
- [Semana_1_Proyecto_2/SalarioPredicción.ipynb](Semana_1_Proyecto_2/SalarioPredicción.ipynb): notebook de entrenamiento, comparacion y guardado del modelo de salario.
- [Semana_1_Proyecto_2/app_salario_streamlit.py](Semana_1_Proyecto_2/app_salario_streamlit.py): aplicacion Streamlit para estimar salario.
- [Semana_1_Proyecto_2/modelo_salario_pipeline.joblib](Semana_1_Proyecto_2/modelo_salario_pipeline.joblib): artefacto de modelo de salario con pipeline y metadata basica.
- [Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb](Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb): notebook de entrenamiento, evaluacion y guardado del modelo de ansiedad.
- [Semana_1_Proyecto_3/stress_SVM.ipynb](Semana_1_Proyecto_3/stress_SVM.ipynb): notebook de entrenamiento, evaluacion y guardado del modelo de estres.
- [Semana_1_Proyecto_3/app_salud_mental_streamlit.py](Semana_1_Proyecto_3/app_salud_mental_streamlit.py): aplicacion Streamlit unificada para evaluar estres y ansiedad.
- [Semana_1_Proyecto_3/rl_model_ansiedad.joblib](Semana_1_Proyecto_3/rl_model_ansiedad.joblib): modelo de ansiedad listo para inferencia.
- [Semana_1_Proyecto_3/svm_classifier_stress.joblib](Semana_1_Proyecto_3/svm_classifier_stress.joblib): modelo de estres listo para inferencia.
- [Semana_1_Proyecto_3/rl_model_ansiedad_metadata.json](Semana_1_Proyecto_3/rl_model_ansiedad_metadata.json): metadata de despliegue del modelo de ansiedad.
- [Semana_1_Proyecto_3/svm_classifier_stress_metadata.json](Semana_1_Proyecto_3/svm_classifier_stress_metadata.json): metadata de despliegue del modelo de estres.
- [requirements.txt](requirements.txt): dependencias del entorno.

## Flujo de trabajo

1. Se carga y prepara la data para cada caso de uso.
2. Se entrena un pipeline con preprocesamiento y modelo.
3. Se compara rendimiento con validacion cruzada.
4. Se selecciona el mejor modelo segun la metrica objetivo.
5. Se guardan artefactos de inferencia.
6. Las apps Streamlit consumen esos artefactos para mostrar resultados al usuario final.

## Como ejecutar

### 1. Crear el entorno virtual

Desde la raiz del repositorio, crear el entorno si aun no existe:

```powershell
python -m venv .venv
```

### 2. Activar el entorno

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

Con el entorno activo, instalar los paquetes del proyecto:

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar las aplicaciones

Con el entorno virtual activo, puedes ejecutar:

```bash
python -m streamlit run Semana_1_Proyecto_1/app_credito_streamlit.py
```

```bash
python -m streamlit run Semana_1_Proyecto_2/app_salario_streamlit.py
```

```bash
python -m streamlit run Semana_1_Proyecto_3/app_salud_mental_streamlit.py
```

### 5. Abrir notebooks

Si quieres revisar el entrenamiento, abre:

- [Semana_1_Proyecto_1/Credito.ipynb](Semana_1_Proyecto_1/Credito.ipynb)
- [Semana_1_Proyecto_2/SalarioPredicción.ipynb](Semana_1_Proyecto_2/SalarioPredicción.ipynb)
- [Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb](Semana_1_Proyecto_3/ansiedad_regresion_logistica.ipynb)
- [Semana_1_Proyecto_3/stress_SVM.ipynb](Semana_1_Proyecto_3/stress_SVM.ipynb)

## Notas

- Los montos en la interfaz estan expresados en soles.
- El modelo de credito y su app se alinean por medio de metadata dedicada.
- El modelo de salario se serializa como un artefacto unico con pipeline y metadata basica.
- Los modelos de salud mental se consumen como artefactos .joblib y se presentan en una unica app Streamlit.
- Las predicciones mostradas son orientativas y no sustituyen una evaluacion formal.
