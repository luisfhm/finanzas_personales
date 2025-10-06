import streamlit as st
from sections.home import render as render_home
from sections.simulador_inflacion import render as render_simulador
from sections.presupuesto import render as render_presupuesto
from sections.deudas import render as render_deudas  # ← ¡AGREGA ESTA LÍNEA!

# Configuración
st.set_page_config(
    page_title="Finanzas Claras",
    page_icon="💡",
    layout="wide"
)

# Estilos CSS (tu bloque completo de CSS aquí)
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Finanzas Claras")
seccion = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio", 
        "📊 Simulador de Inflación", 
        "💰 Presupuesto Inteligente",
        "💳 Manejo de Deudas"  # ← ¡AGREGA ESTA LÍNEA!
    ],
    index=0
)

# Router
if seccion == "🏠 Inicio":
    render_home()
elif seccion == "📊 Simulador de Inflación":
    render_simulador()
elif seccion == "💰 Presupuesto Inteligente":
    render_presupuesto()
elif seccion == "💳 Manejo de Deudas": 
    render_deudas()
# Footer (global)
# ----------------------
st.markdown(
    """
    <div class="footer">
        © 2025 Finanzas Educativas | Herramienta con fines didácticos | 
        <a href="#" style="color: #7f8c8d; text-decoration: none;">Términos y condiciones</a> | 
        <a href="#" style="color: #7f8c8d; text-decoration: none;">Política de privacidad</a>
    </div>
    """,
    unsafe_allow_html=True
)