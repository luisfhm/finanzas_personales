import streamlit as st
import pandas as pd
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.graficas import plot_ahorro

# ----------------------
# Estilos CSS personalizados
# ----------------------
st.markdown(
    """
    <style>
    /* Fondo y fuente general */
    .stApp {
        background-color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
    }

    /* Título principal */
    h1 {
        color: #1f4e79;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }

    /* Secciones como tarjetas */
    .stContainer {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Inputs */
    .stNumberInput input {
        border-radius: 8px;
        padding: 6px;
        border: 1px solid #ccc;
    }

    /* Botones */
    .stButton>button {
        background-color: #1f4e79;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #3a6ea5;
        cursor: pointer;
    }

    /* Textos de resultados */
    .stMarkdown p, .stMarkdown span {
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Gráfica */
    .element-container:nth-child(6) {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Logo y título
# ----------------------
st.image("assets/logo.png", width=150)
st.title("Simulador Educativo de Finanzas Personales")

# ----------------------
# Entradas
# ----------------------
salario = st.number_input("Salario mensual:", value=10000, format="%d")
ahorro_mensual = st.number_input("Ahorro mensual:", value=2000, format="%d")
años = st.number_input("Años:", value=5, format="%d")
inflacion_prom = st.slider("Inflación anual (%)", 0.0, 20.0, 4.0)

# Mostrar inputs en formato pesos
st.write("💰 Salario mensual:", f"${salario:,.0f}")
st.write("💵 Ahorro mensual:", f"${ahorro_mensual:,.0f}")

# ----------------------
# Cálculos
# ----------------------
meses = años*12
inflacion_mensual = (1 + inflacion_prom/100)**(1/12) - 1
ahorro_colchon = ahorro_total(ahorro_mensual, meses)
poder_colchon = poder_adquisitivo(ahorro_colchon, inflacion_mensual)

# DataFrame
df = pd.DataFrame({
    "Mes": range(1, meses+1),
    "Ahorro debajo del colchón": ahorro_colchon,
    "Poder adquisitivo colchón": poder_colchon
})

# ----------------------
# Resultados finales
# ----------------------
st.write("💰 Ahorro debajo del colchón (final):", f"${ahorro_colchon[-1]:,.0f}")
st.write("💸 Poder adquisitivo (final):", f"${poder_colchon[-1]:,.0f}")

# ----------------------
# Gráfica
# ----------------------
fig = plot_ahorro(df)
st.plotly_chart(fig, use_container_width=True)