# sections/presupuesto.py
import streamlit as st

def render():
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
            deseos = st.number_input("🎉 Deseos ($)", min_value=0, value=min(int(ingreso * 0.3), max(0, ingreso - necesidades)), step=100, format="%d")
        with col3:
            ahorro_inv = st.number_input("📈 Ahorro/Inversión ($)", min_value=0, value=min(int(ingreso * 0.2), max(0, ingreso - necesidades - deseos)), step=100, format="%d")

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