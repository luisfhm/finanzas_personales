import streamlit as st
import pandas as pd
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.graficas import plot_ahorro

# ----------------------
# Configuración general
# ----------------------
st.set_page_config(
    page_title="Finanzas Claras",
    page_icon="💡",
    layout="wide"
)

# ----------------------
# Estilos CSS personalizados (mejorados)
# ----------------------
st.markdown(
    """
    <style>
    /* ... (todo lo anterior igual hasta "Métricas: estilo base") ... */

    /* --- Métricas: estilo base --- */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
        text-align: center;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #264653 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: bold !important;
    }

    /* --- Colores por contenedor --- */
    .metric-ahorro div[data-testid="stMetricValue"] {
        color: #2a9d8f !important;
    }

    .metric-poder div[data-testid="stMetricValue"] {
        color: #e76f51 !important;
    }

    /* ... (el resto del CSS igual: botones, inputs, etc.) ... */
    </style>
    """,
    unsafe_allow_html=True
)
# ----------------------
# Sidebar (menú de navegación)
# ----------------------
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("Finanzas Claras")

seccion = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "📊 Simulador de Inflación", "💰 Presupuesto Inteligente"],
    index=0
)

# ----------------------
# PÁGINA DE INICIO (nueva sección principal)
# ----------------------
if seccion == "🏠 Inicio":
    # Cabecera
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/logo.png", width=100)
    with col2:
        st.title("Finanzas Claras")
        st.markdown("### Toma el control de tu dinero, sin tecnicismos")

    st.markdown(
        """
        <div style='background-color:#e8f4fc; padding:20px; border-radius:12px; margin:25px 0;'>
        <p style='font-size:1.2rem; color:#003366; margin:0;'>
        💡 <strong>¿Sabías que la inflación puede borrar hasta el 40% del valor de tu ahorro en 10 años?</strong><br>
        En Finanzas Claras, te ayudamos a entender tus finanzas personales con herramientas simples, visuales y gratuitas.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Beneficios
    st.subheader("✨ ¿Qué puedes hacer hoy?")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(
            """
            <div class="feature-card">
                <h4>📊 Simulador de Inflación</h4>
                <p>Descubre cuánto pierde tu ahorro con el paso del tiempo.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col_b:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🎯 Próximamente: Metas Financieras</h4>
                <p>Planea tu fondo de emergencia, viaje o auto con pasos claros.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Llamado a la acción
    st.markdown("<br>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🚀 Probar el Simulador de Inflación"):
            st.session_state.seccion = "Simulador de Inflación"
            st.rerun()  # Opcional: redirige (pero Streamlit no tiene router nativo)

    # Filosofía — con formato premium y centrado
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='
            max-width: 800px;
            margin: 0 auto;
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #e9ecef;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
            text-align: center;
            color: #1a1a1a;
            font-size: 1.25rem;
            line-height: 1.7;
        '>
            <h3 style='
                color: #0d3b66;
                margin-top: 0;
                margin-bottom: 20px;
                font-weight: 700;
                font-size: 1.6rem;
            '>🎓 Nuestra misión</h3>
            <p style='margin: 10px 0;'>
                Democratizar la educación financiera en México.
            </p>
            <p style='margin: 10px 0; font-weight: 600; color: #0d3b66;'>
                No vendemos productos. No tenemos afiliaciones.
            </p>
            <p style='margin: 10px 0;'>
                Solo queremos que entiendas tu dinero.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------
# SIMULADOR DE INFLACIÓN (como sección secundaria)
# ----------------------
elif seccion == "📊 Simulador de Inflación":
    st.title("📊 Simulador de Ahorro e Inflación")
    st.markdown("Aprende cómo la **inflación afecta tu ahorro** de manera simple y visual.")

    # Parámetros
    st.subheader("⚙️ Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        salario = st.number_input("💰 Salario mensual:", value=10000, format="%d")
        años = st.number_input("📆 Años:", value=5, format="%d")
    with col2:
        ahorro_mensual = st.number_input("💵 Ahorro mensual:", value=2000, format="%d")
        inflacion_prom = st.slider("📈 Inflación anual (%)", 0.0, 20.0, 4.0)

    # Cálculos
    meses = años * 12
    inflacion_mensual = (1 + inflacion_prom / 100) ** (1 / 12) - 1
    ahorro_colchon = ahorro_total(ahorro_mensual, meses)
    poder_colchon = poder_adquisitivo(ahorro_colchon, inflacion_mensual)

    df = pd.DataFrame({
        "Mes": range(1, meses + 1),
        "Ahorro nominal": ahorro_colchon,
        "Poder adquisitivo real": poder_colchon
    })

    # Resultados finales — personalizados
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-label">💰 Ahorro final</div>
                <div class="metric-value" style="color: #2a9d8f;">${ahorro_colchon[-1]:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="custom-metric">
                <div class="metric-label">💸 Poder adquisitivo final</div>
                <div class="metric-value" style="color: #e76f51;">${poder_colchon[-1]:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
    f"""
    <div style='
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        color: #1a1a1a;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 25px 0;
    '>
        En <b>{años} años</b>, si ahorras <b style="color:#2a9d8f">${ahorro_mensual:,.0f}</b> cada mes, 
        acumularás <b style="color:#2a9d8f">${ahorro_colchon[-1]:,.0f}</b>.<br>
        Pero por la inflación, ese monto tendrá un poder adquisitivo de solo 
        <b style="color:#e76f51">${poder_colchon[-1]:,.0f}</b> en pesos de hoy.
    </div>
    """,
    unsafe_allow_html=True)

    # Gráfica — con colores de marca y alto contraste
    import plotly.graph_objects as go

    fig = go.Figure()

    # Línea 1: Ahorro nominal (verde azulado)
    fig.add_trace(go.Scatter(
        x=df["Mes"],
        y=df["Ahorro nominal"],
        mode='lines',
        name='Ahorro nominal',
        line=dict(color='#2a9d8f', width=3)
    ))

    # Línea 2: Poder adquisitivo real (coral)
    fig.add_trace(go.Scatter(
        x=df["Mes"],
        y=df["Poder adquisitivo real"],
        mode='lines',
        name='Poder adquisitivo real',
        line=dict(color='#e76f51', width=3, dash='dot')
    ))

    fig.update_layout(
        title=dict(
            text="Evolución del ahorro vs inflación",
            font=dict(size=22, color="#1a1a1a", weight="bold")
        ),
        xaxis=dict(
            title=dict(text="Mes", font=dict(size=16, color="#1a1a1a")),
            tickfont=dict(size=14, color="#4a4a4a"),
            showgrid=True,
            gridcolor="#eaeaea"
        ),
        yaxis=dict(
            title=dict(text="Pesos", font=dict(size=16, color="#1a1a1a")),
            tickfont=dict(size=14, color="#4a4a4a"),
            showgrid=True,
            gridcolor="#eaeaea",
            tickformat="$,.0f"
        ),
        legend=dict(
            title=dict(text="Escenario", font=dict(size=14, color="#264653")),
            font=dict(size=13, color="#1a1a1a"),
            bgcolor="rgba(248,249,250,0.7)",
            bordercolor="#e9ecef",
            borderwidth=1
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(t=50, b=50, l=50, r=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insight educativo
    diferencia = ahorro_colchon[-1] - poder_colchon[-1]
    if diferencia > 0:
        st.info(f"💡 **Reflexión:** La inflación ha erosionado **${diferencia:,.0f}** de tu ahorro. Esto es por qué ahorrar no es suficiente: necesitas invertir.")

# ----------------------
# SECCIÓN: Presupuesto Inteligente
# ----------------------
elif seccion == "💰 Presupuesto Inteligente":
    st.title("💰 Presupuesto Inteligente (Regla 50/30/20)")
    st.markdown("""
    <div style='background-color:#f0f7ff; padding:18px; border-radius:12px; margin-bottom:25px; border:1px solid #cce5ff;'>
        <p style='margin:0; color:#0d3b66; font-size:1.15rem;'>
        📌 La regla 50/30/20 es una guía simple para equilibrar tus finanzas:
        </p>
        <ul style='margin-top:10px; color:#1a1a1a;'>
            <li><strong>50%</strong> en <strong>necesidades</strong> (vivienda, comida, transporte)</li>
            <li><strong>30%</strong> en <strong>deseos</strong> (entretenimiento, suscripciones, viajes)</li>
            <li><strong>20%</strong> en <strong>ahorro e inversión</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Ingreso mensual
    ingreso = st.number_input("💼 Ingreso mensual neto ($)", min_value=0, value=15000, step=500, format="%d")
    
    if ingreso > 0:
        st.subheader("📝 Ingresa tus gastos mensuales")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            necesidades = st.number_input("🏠 Necesidades ($)", min_value=0, value=min(int(ingreso * 0.5), ingreso), step=100, format="%d")
        with col2:
            deseos = st.number_input("🎉 Deseos ($)", min_value=0, value=min(int(ingreso * 0.3), ingreso - necesidades), step=100, format="%d")
        with col3:
            ahorro_inv = st.number_input("📈 Ahorro/Inversión ($)", min_value=0, value=min(int(ingreso * 0.2), ingreso - necesidades - deseos), step=100, format="%d")

        total_gastos = necesidades + deseos + ahorro_inv
        sobrante = ingreso - total_gastos

        # Calcular porcentajes reales
        pct_nec = (necesidades / ingreso * 100) if ingreso > 0 else 0
        pct_des = (deseos / ingreso * 100) if ingreso > 0 else 0
        pct_ah = (ahorro_inv / ingreso * 100) if ingreso > 0 else 0

        # Mostrar diagnóstico
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔍 Diagnóstico de tu presupuesto")

        # Métricas personalizadas
        col1, col2, col3 = st.columns(3)
        with col1:
            color_nec = "#2a9d8f" if pct_nec <= 50 else "#e76f51"
            icon_nec = "✅" if pct_nec <= 50 else "⚠️"
            st.markdown(
                f"""
                <div class="custom-metric">
                    <div class="metric-label">🏠 Necesidades</div>
                    <div class="metric-value" style="color: {color_nec};">{pct_nec:.0f}%</div>
                    <div style="font-size: 0.95rem; color: #555;">{icon_nec} Ideal: ≤50%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            color_des = "#2a9d8f" if pct_des <= 30 else "#e76f51"
            icon_des = "✅" if pct_des <= 30 else "⚠️"
            st.markdown(
                f"""
                <div class="custom-metric">
                    <div class="metric-label">🎉 Deseos</div>
                    <div class="metric-value" style="color: {color_des};">{pct_des:.0f}%</div>
                    <div style="font-size: 0.95rem; color: #555;">{icon_des} Ideal: ≤30%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            color_ah = "#2a9d8f" if pct_ah >= 20 else "#e76f51"
            icon_ah = "✅" if pct_ah >= 20 else "⚠️"
            st.markdown(
                f"""
                <div class="custom-metric">
                    <div class="metric-label">📈 Ahorro/Inversión</div>
                    <div class="metric-value" style="color: {color_ah};">{pct_ah:.0f}%</div>
                    <div style="font-size: 0.95rem; color: #555;">{icon_ah} Ideal: ≥20%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Recomendación final
        st.markdown("<br>", unsafe_allow_html=True)
        if sobrante > 0:
            st.success(f"✅ ¡Excelente! Te sobran **${sobrante:,.0f}**. ¿Los destinarás a metas o inversión?")
        elif sobrante < 0:
            st.error(f"⚠️ Estás gastando **${-sobrante:,.0f}** más de lo que ganas. Revisa tus gastos.")
        else:
            st.info("💡 Tu presupuesto está equilibrado. ¡Sigue así!")

        # Insight educativo
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Consejo práctico:** Si tus necesidades superan el 50%, considera opciones como renta compartida, transporte público o reducir suscripciones innecesarias.")
    else:
        st.info("👉 Ingresa tu ingreso mensual para comenzar a construir tu presupuesto.")
# ----------------------
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