# sections/simulador_inflacion.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.calculos import ahorro_total, poder_adquisitivo
from functions.datos import obtener_inflacion_mx

def render():
    st.title("📊 Simulador de Ahorro e Inflación")
    st.markdown("Aprende cómo la **inflación afecta tu ahorro** de manera simple y visual.")

    # --- Obtener inflación real desde Banxico ---
    ultima_fecha, inflacion_actual = obtener_inflacion_mx()
    
    if inflacion_actual is not None:
        fuente = "Banxico / INEGI"
        st.markdown(
            f"""
            <div style='
                background-color: #f0f7ff;
                padding: 15px;
                border-radius: 12px;
                border: 1px solid #cce5ff;
                color: #0d3b66;
                font-size: 1.05rem;
                margin-bottom: 20px;
            '>
                📌 <strong>Inflación anual en México ({ultima_fecha}): {inflacion_actual:.2f}%</strong><br>
                <span style="font-size: 0.95rem; color: #555;">Fuente: {fuente}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        valor_default = inflacion_actual
    else:
        st.warning("⚠️ No se pudo obtener la inflación actual. Usando 4.0% como referencia.")
        valor_default = 4.0

    # Parámetros
    st.subheader("⚙️ Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        salario = st.number_input("💰 Salario mensual:", value=10000, format="%d")
        años = st.number_input("📆 Años:", value=5, format="%d")
    with col2:
        ahorro_mensual = st.number_input("💵 Ahorro mensual:", value=2000, format="%d")
        inflacion_prom = st.slider(
            "📈 Inflación anual (%)",
            0.0,
            20.0,
            float(valor_default),
            step=0.1
        )

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