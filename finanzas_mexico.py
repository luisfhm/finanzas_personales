# archivo: finanzas_mexico.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Título ---
st.title("Simulador Educativo de Finanzas Personales (México)")
st.write("""
Este simulador te ayuda a entender cómo la inflación y tus ahorros afectan tu poder adquisitivo en México.
""")

# --- Entradas del usuario ---
salario = st.number_input("Ingresa tu ingreso mensual (MXN):", min_value=0, value=10000, step=500)
ahorro_mensual = st.number_input("Cantidad que puedes ahorrar al mes (MXN):", min_value=0, value=2000, step=500)
años = st.number_input("Horizonte de tiempo (años):", min_value=1, max_value=50, value=5)

inflacion_promedio = st.slider("Inflación promedio anual (%)", min_value=0.0, max_value=20.0, value=4.0, step=0.1)
rendimiento_inversion = st.slider("Rendimiento promedio anual de inversión (%)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)

# --- Cálculos ---
meses = años * 12
inflacion_mensual = (1 + inflacion_promedio/100) ** (1/12) - 1
rendimiento_mensual = (1 + rendimiento_inversion/100) ** (1/12) - 1

# Inicialización de listas para evolución
ahorro_colchon = []
ahorro_inversion = []
poder_adquisitivo_colchon = []
poder_adquisitivo_inversion = []

total_colchon = 0
total_inversion = 0

for i in range(1, meses+1):
    total_colchon += ahorro_mensual
    total_inversion = total_inversion*(1+rendimiento_mensual) + ahorro_mensual

    # Ajuste por inflación
    poder_adquisitivo_colchon.append(total_colchon / ((1 + inflacion_mensual) ** i))
    poder_adquisitivo_inversion.append(total_inversion / ((1 + inflacion_mensual) ** i))
    ahorro_colchon.append(total_colchon)
    ahorro_inversion.append(total_inversion)

# --- DataFrame para mostrar
df = pd.DataFrame({
    "Mes": range(1, meses+1),
    "Ahorro debajo del colchón": ahorro_colchon,
    "Ahorro con inversión": ahorro_inversion,
    "Poder adquisitivo colchón": poder_adquisitivo_colchon,
    "Poder adquisitivo inversión": poder_adquisitivo_inversion
})

# --- Gráficas ---
st.subheader("Evolución del ahorro")
fig, ax = plt.subplots()
ax.plot(df["Mes"], df["Ahorro debajo del colchón"], label="Colchón")
ax.plot(df["Mes"], df["Ahorro con inversión"], label="Inversión")
ax.set_xlabel("Meses")
ax.set_ylabel("MXN")
ax.legend()
st.pyplot(fig)

st.subheader("Poder adquisitivo ajustado por inflación")
fig2, ax2 = plt.subplots()
ax2.plot(df["Mes"], df["Poder adquisitivo colchón"], label="Colchón")
ax2.plot(df["Mes"], df["Poder adquisitivo inversión"], label="Inversión")
ax2.set_xlabel("Meses")
ax2.set_ylabel("MXN ajustados por inflación")
ax2.legend()
st.pyplot(fig2)

# --- Mensaje educativo ---
st.markdown("""
### Consejos educativos:
- Ahorrar sin invertir puede hacer que pierdas poder adquisitivo con el tiempo debido a la inflación.
- Invertir de manera conservadora puede ayudarte a mantener y aumentar tu dinero real.
- Incluso cantidades pequeñas de ahorro mensual, si se invierten consistentemente, pueden crecer significativamente.
""")
