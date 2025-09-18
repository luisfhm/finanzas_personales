import streamlit as st
import pandas as pd
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.graficas import plot_ahorro

# Configuración inicial
st.title("Simulador Educativo de Finanzas Personales")

# Entradas
salario = st.number_input("Salario mensual:", value=10000)
ahorro_mensual = st.number_input("Ahorro mensual:", value=2000)
años = st.number_input("Años:", value=5)
inflacion_prom = st.slider("Inflación anual (%)", 0.0, 20.0, 4.0)

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

# Gráfica
st.pyplot(plot_ahorro(df))