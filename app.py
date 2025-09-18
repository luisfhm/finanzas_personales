import streamlit as st
import pandas as pd
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.graficas import plot_ahorro

# Logo y título
st.image("assets/logo.png", width=150)
st.title("Simulador Educativo de Finanzas Personales")

# Entradas
salario = st.number_input("Salario mensual:", value=10000, format="%d")
ahorro_mensual = st.number_input("Ahorro mensual:", value=2000, format="%d")
años = st.number_input("Años:", value=5, format="%d")
inflacion_prom = st.slider("Inflación anual (%)", 0.0, 20.0, 4.0)

# Mostrar inputs en formato pesos
st.write("💰 Salario mensual:", f"${salario:,.0f}")
st.write("💵 Ahorro mensual:", f"${ahorro_mensual:,.0f}")

# Cálculos
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

# Mostrar valores finales
st.write("💰 Ahorro debajo del colchón (final):", f"${ahorro_colchon[-1]:,.0f}")
st.write("💸 Poder adquisitivo (final):", f"${poder_colchon[-1]:,.0f}")

# Gráfica
st.pyplot(plot_ahorro(df))
