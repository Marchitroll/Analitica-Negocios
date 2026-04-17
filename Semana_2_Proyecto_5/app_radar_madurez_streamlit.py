import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Correr:
# python -m streamlit run Semana_2_Proyecto_5/app_radar_madurez_streamlit.py

DIMENSIONES = [
	"Calidad de datos",
	"Roles y responsabilidades",
	"Politicas y normativas",
	"Seguridad y privacidad",
	"Cultura de datos",
]

NIVEL_MIN = 1
NIVEL_MAX = 5
NIVELES_RADIALES = list(range(NIVEL_MIN, NIVEL_MAX + 1))


def configurar_pagina() -> None:
	st.set_page_config(
		page_title="Radar de Madurez",
		page_icon=":bar_chart:",
		layout="wide",
	)


def inicializar_estado() -> None:
	if "niveles_actuales" not in st.session_state:
		st.session_state.niveles_actuales = [2, 1, 1, 2, 2]

	if "niveles_objetivo" not in st.session_state:
		st.session_state.niveles_objetivo = [5, 5, 5, 5, 5]


def cerrar_poligono(valores: list[int]) -> list[int]:
	return valores + [valores[0]]


def construir_radar(labels: list[str], actuales: list[int], objetivos: list[int]):
	angulos = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
	angulos_cerrados = cerrar_poligono(angulos)
	actuales_cerrados = cerrar_poligono(actuales)
	objetivos_cerrados = cerrar_poligono(objetivos)

	fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})

	ax.plot(angulos_cerrados, actuales_cerrados, color="#D1495B", linewidth=2, label="Nivel actual")
	ax.fill(angulos_cerrados, actuales_cerrados, color="#D1495B", alpha=0.25)

	ax.plot(angulos_cerrados, objetivos_cerrados, color="#2A9D8F", linewidth=2, linestyle="--", label="Nivel objetivo")
	ax.fill(angulos_cerrados, objetivos_cerrados, color="#2A9D8F", alpha=0.18)

	ax.set_yticks(NIVELES_RADIALES)
	ax.set_yticklabels([str(nivel) for nivel in NIVELES_RADIALES])
	ax.set_ylim(NIVEL_MIN, NIVEL_MAX)
	ax.set_xticks(angulos)
	ax.set_xticklabels(labels, fontsize=10)
	ax.set_title("Diagnostico de Madurez del Gobierno de Datos", size=14, weight="bold")
	ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))

	return fig


def renderizar_controles() -> tuple[list[int], list[int]]:
	st.sidebar.header("Niveles de madurez")
	st.sidebar.caption("Define el estado actual y el objetivo por dimension.")

	niveles_actuales = []
	niveles_objetivo = []

	for i, dimension in enumerate(DIMENSIONES):
		st.sidebar.markdown(f"**{dimension}**")

		nivel_actual = st.sidebar.slider(
			label=f"Actual {i + 1}",
			min_value=NIVEL_MIN,
			max_value=NIVEL_MAX,
			value=st.session_state.niveles_actuales[i],
			key=f"actual_{i}",
		)
		nivel_objetivo = st.sidebar.slider(
			label=f"Objetivo {i + 1}",
			min_value=NIVEL_MIN,
			max_value=NIVEL_MAX,
			value=st.session_state.niveles_objetivo[i],
			key=f"objetivo_{i}",
		)

		niveles_actuales.append(nivel_actual)
		niveles_objetivo.append(nivel_objetivo)

	return niveles_actuales, niveles_objetivo


def renderizar_resumen(actuales: list[int], objetivos: list[int]) -> None:
	promedio_actual = float(np.mean(actuales))
	promedio_objetivo = float(np.mean(objetivos))

	col1, col2, col3 = st.columns(3)
	col1.metric("Promedio actual", f"{promedio_actual:.2f}")
	col2.metric("Promedio objetivo", f"{promedio_objetivo:.2f}")
	col3.metric("Brecha promedio", f"{(promedio_objetivo - promedio_actual):.2f}")


def main() -> None:
	configurar_pagina()
	inicializar_estado()

	st.title("Radar de Madurez")
	st.caption("Actualiza los niveles desde la barra lateral y observa el radar en tiempo real.")

	niveles_actuales, niveles_objetivo = renderizar_controles()
	st.session_state.niveles_actuales = niveles_actuales
	st.session_state.niveles_objetivo = niveles_objetivo

	renderizar_resumen(niveles_actuales, niveles_objetivo)

	figura = construir_radar(DIMENSIONES, niveles_actuales, niveles_objetivo)
	st.pyplot(figura, clear_figure=True)


if __name__ == "__main__":
	main()