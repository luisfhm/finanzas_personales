import streamlit as st
import pandas as pd
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.graficas import plot_ahorro

# ----------------------
# Configuración general
# ----------------------
st.set_page_config(
    page_title="Simulador Finanzas Personales",
    page_icon="💸",
    layout="wide"
)

# ----------------------
# Estilos CSS personalizados
# ----------------------
st.markdown(
    """
    <style>
    /* Fondo y texto de los metric cards */
    div[data-testid="stMetricValue"] {
        color: #1f4e79 !important; /* texto principal */
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #2c3e50 !important; /* etiqueta */
        font-size: 1rem !important;
    }

    /* Fondo del contenedor */
    div[data-testid="stMetric"] {
        background-color: #f7f9fc; /* gris muy claro */
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------
# Sidebar (estructura modular)
# ----------------------
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Menú de navegación")

seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ["Simulador de ahorro", "Deudas", "Inversiones", "Educación financiera 📚"],
    index=0
)

# ----------------------
# Sección 1: Simulador de ahorro
# ----------------------
if seccion == "Simulador de ahorro":
    st.title("📊 Simulador de Ahorro e Inflación")
    st.markdown("Aprende cómo la **inflación afecta tu ahorro** de manera simple y visual.")

    # Parámetros de simulación
    st.subheader("⚙️ Parámetros")
    salario = st.number_input("💰 Salario mensual:", value=10000, format="%d")
    ahorro_mensual = st.number_input("💵 Ahorro mensual:", value=2000, format="%d")
    años = st.number_input("📆 Años:", value=5, format="%d")
    inflacion_prom = st.slider("📈 Inflación anual (%)", 0.0, 20.0, 4.0)

    # Cálculos
    meses = años * 12
    inflacion_mensual = (1 + inflacion_prom / 100) ** (1 / 12) - 1
    ahorro_colchon = ahorro_total(ahorro_mensual, meses)
    poder_colchon = poder_adquisitivo(ahorro_colchon, inflacion_mensual)

    df = pd.DataFrame({
        "Mes": range(1, meses + 1),
        "Ahorro debajo del colchón": ahorro_colchon,
        "Poder adquisitivo colchón": poder_colchon
    })
    st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        color: #003366 !important;  /* Azul oscuro */
        font-weight: bold;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    # Resultados finales
    col1, col2 = st.columns(2)
    col1.metric("💰 Ahorro final", f"${ahorro_colchon[-1]:,.0f}")
    col2.metric("💸 Poder adquisitivo final", f"${poder_colchon[-1]:,.0f}")

    st.markdown(
    f"""
    <div style='
        background-color:#f0f8ff;
        padding:15px;
        border-radius:10px;
        border:1px solid #a3c4f3;
        color:#003366;
        font-size:16px;
    '>
        En <b>{años} años</b>, si ahorras <b>${ahorro_mensual:,.0f}</b> cada mes,
        tendrás un total de <b>${ahorro_colchon[-1]:,.0f}</b>. 
        Pero por la inflación, ese dinero equivale a 
        <b>${poder_colchon[-1]:,.0f}</b> en pesos actuales.
    </div>
    """,
    unsafe_allow_html=True
)




    # Gráfica
    fig = plot_ahorro(df)
    fig.update_layout(
    title=dict(
        text="Evolución del ahorro vs inflación",
        font=dict(size=20, color="#003366")
    ),
    xaxis=dict(
        title=dict(text="Mes", font=dict(size=16, color="#000000")),
        tickfont=dict(size=14, color="#000000")
    ),
    yaxis=dict(
        title=dict(text="Pesos", font=dict(size=16, color="#000000")),
        tickfont=dict(size=14, color="#000000")
    ),
    legend=dict(
        title=dict(text="Escenario", font=dict(size=14, color="#003366")),
        font=dict(size=12, color="#000000")
    ),
    template="plotly_white"
)

    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Sección 2: Deudas (placeholder)
# ----------------------
elif seccion == "Deudas":
    st.title("💳 Manejo de Deudas")
    st.warning("🚧 Esta sección está en construcción. Próximamente podrás simular el impacto de tus deudas.")

# ----------------------
# Sección 3: Inversiones (placeholder)
# ----------------------
elif seccion == "Inversiones":
    st.title("📈 Simulador de Inversiones")
    st.warning("🚧 Aquí podrás comparar diferentes escenarios de inversión.")

# ----------------------
# Sección 4: Educación financiera (placeholder)
# ----------------------
elif seccion == "Educación financiera 📚":
    st.title("📚 Educación Financiera")
    st.markdown("Tips, artículos y explicaciones sencillas sobre conceptos de dinero.")
