# 🧠 Analítica de Negocios - Proyectos

Repositorio de proyectos de analítica aplicada y Machine Learning organizada por semanas. Cada proyecto sigue un flujo reproducible de exploración, modelado, validación de no fuga de datos (*data leakage*), serialización de artefactos y consumo desde aplicaciones Streamlit.


> **Entorno de ejecución principal:** Python `3.13.9` administrado mediante el entorno Conda `base` o entorno virtual `.venv` compatible. Las librerías de modelado y visualización se detallan en el archivo [requirements.txt](requirements.txt).
---

## 🛠️ Instrucciones de Ejecución

### 1. Preparación del Entorno

Puedes utilizar un entorno virtual estándar de Python o el entorno Conda `base` recomendado.

**Opción A: Creación de entorno virtual tradicional**
```powershell
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activar en PowerShell (Windows)
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt
```

**Opción B: Uso del entorno Conda base**
```powershell
# Activar entorno base
conda activate base
```

### 2. Ejecución de las Aplicaciones de Streamlit

Para iniciar cualquier app Streamlit desde la raíz del repositorio, usa la sintaxis general:

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

* **Auto-reporte y Orientación**: Las evaluaciones de salud mental son herramientas informativas y educativas. No sustituyen un diagnóstico clínico profesional.
