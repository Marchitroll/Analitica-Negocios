# 🧠 Analítica de Negocios - Proyectos

Repositorio de proyectos de analítica aplicada y Machine Learning organizada por semanas. Cada proyecto sigue un flujo reproducible de exploración, modelado, validación de no fuga de datos (*data leakage*), serialización de artefactos y consumo desde aplicaciones Streamlit.

> **Entorno de ejecución principal:** Python `3.13.9` administrado mediante un entorno Conda dedicado (ej. `analitica` o `dl` para proyectos de PySpark). Las librerías de modelado y visualización se detallan en el archivo [requirements.txt](requirements.txt).

---

## 🛠️ Instrucciones de Ejecución

### 1. Preparación del Entorno

Para una correcta y estable ejecución, se recomienda utilizar **Anaconda** para administrar los entornos y dependencias de Python.

**Paso 1: Descargar e instalar Anaconda**
Descargar la versión correspondiente para el sistema operativo desde la [Página Oficial de Anaconda](https://www.anaconda.com/download).

**Paso 2: Crear y activar un nuevo entorno Conda**
Abrir la terminal (o Anaconda Prompt) y ejecutar los siguientes comandos para crear un entorno virtual limpio y dedicado:

```powershell
# 1. Crear el entorno conda (ej. "analitica")
conda create -n analitica python=3.13.9 -y

# 2. Activar el entorno
conda activate analitica
```

**Paso 3: Instalar las dependencias generales**
Una vez activado el entorno, instalar todas las librerías base especificadas en el archivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

**Nota para el Proyecto de Big Data (Semana 8 - Proyecto 10):**
Este proyecto de Big Data requiere de **Java 21** para ejecutar PySpark. Dado que la librería `pyspark` ya está incluida de forma predeterminada en el archivo `requirements.txt` (e instalada en el Paso 3), asegurar que Java 21 esté instalado de forma aislada y local en el entorno conda activo:

```powershell
# Instalar Java 21 de forma aislada en el entorno activo
conda install -y openjdk=21
```

### 2. Ejecución de las Aplicaciones de Streamlit

Para iniciar cualquier aplicación de Streamlit desde la raíz del repositorio, utilizar la siguiente sintaxis general:

```powershell
# Sintaxis general
python -m streamlit run <RUTA/AL/ARCHIVO_APP>.py

# Ejemplos
python -m streamlit run Semana_1_Proyecto_1/app_credito_streamlit.py
python -m streamlit run Semana_1_Proyecto_2/app_salario_streamlit.py
python -m streamlit run Semana_1_Proyecto_4/app_chatbot_streamlit.py
python -m streamlit run Semana_7_Proyecto_9/app.py
```

---

## 📝 Notas

- **Auto-reporte y Orientación**: Las evaluaciones de salud mental son herramientas informativas y educativas. No sustituyen un diagnóstico clínico profesional.
