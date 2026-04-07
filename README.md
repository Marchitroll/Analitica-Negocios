# Analitica de Negocios - Mini Proyecto de Credito

Este mini proyecto aplica analitica de negocios para construir y desplegar un modelo simple de evaluacion crediticia. La idea central es transformar datos de clientes en una decision de aprobacion o rechazo, apoyada por un flujo reproducible de entrenamiento y una interfaz ligera para consumo.

## Objetivo de negocio

El objetivo es ayudar a una entidad financiera a tomar decisiones preliminares de credito con mayor consistencia. En lugar de evaluar casos manualmente uno por uno, el proyecto utiliza un modelo de clasificacion que estima la probabilidad de aprobacion y devuelve una decision interpretable para el usuario.

## Enfoque analitico

El proyecto se estructuro con buenas practicas de analitica predictiva:

- Separacion clara entre entrenamiento y despliegue.
- Preprocesamiento dentro de un pipeline para evitar fuga de informacion.
- Validacion con particion estratificada y metricas orientadas a clasificacion.
- Seleccion del mejor modelo usando ROC-AUC como criterio principal.
- Persistencia del modelo y de su metadata para asegurar consistencia entre entrenamiento e inferencia.

## Componentes del proyecto

- [Semana_1_Proyecto_1/Credito.ipynb](Semana_1_Proyecto_1/Credito.ipynb): notebook de entrenamiento, evaluacion y guardado del modelo.
- [Semana_1_Proyecto_1/app_credito_streamlit.py](Semana_1_Proyecto_1/app_credito_streamlit.py): aplicacion Streamlit para capturar datos y generar una prediccion.
- [Semana_1_Proyecto_1/model_credito.joblib](Semana_1_Proyecto_1/model_credito.joblib): modelo entrenado listo para inferencia.
- [Semana_1_Proyecto_1/model_credito_metadata.json](Semana_1_Proyecto_1/model_credito_metadata.json): contrato de despliegue con columnas, etiquetas y versiones.
- [requirements.txt](requirements.txt): dependencias del entorno.

## Flujo de trabajo

1. Se carga y prepara la data de credito.
2. Se entrena un pipeline con preprocesamiento y clasificador.
3. Se compara rendimiento con validacion cruzada.
4. Se selecciona el mejor modelo segun ROC-AUC.
5. Se guarda el modelo y su metadata.
6. La app Streamlit consume esos artefactos para mostrar una decision al usuario final.

## Interpretacion de la solucion

Desde una perspectiva de negocio, este proyecto no busca reemplazar una politica crediticia formal. Su valor esta en estandarizar una primera decision, reducir friccion operativa y ofrecer una base analitica repetible para discutir riesgo, aprobacion y segmentacion de clientes.

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

### 4. Ejecutar la aplicacion

Con el entorno virtual del proyecto activo, iniciar la aplicacion con:

```bash
python -m streamlit run Semana_1_Proyecto_1/app_credito_streamlit.py
```

### 5. Abrir el notebook

Si quieres revisar el entrenamiento, abre [Semana_1_Proyecto_1/Credito.ipynb](Semana_1_Proyecto_1/Credito.ipynb) en Jupyter con el mismo entorno activo.

## Notas

- Los montos en la interfaz estan expresados en soles.
- El modelo y la app fueron ajustados para mantenerse alineados mediante metadata.
- La prediccion mostrada es orientativa y no sustituye una evaluacion crediticia formal.
