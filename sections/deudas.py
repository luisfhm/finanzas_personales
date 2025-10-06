# sections/deudas.py
import streamlit as st
import pandas as pd
import numpy as np

def calcular_pago_bola_nieve(deudas, pago_mensual):
    """Estrategia: pagar primero la deuda con menor saldo"""
    deudas = sorted(deudas, key=lambda x: x["saldo"])  # ordenar por saldo
    return simular_pago(deudas, pago_mensual)

def calcular_pago_avalancha(deudas, pago_mensual):
    """Estrategia: pagar primero la deuda con mayor tasa de interés"""
    deudas = sorted(deudas, key=lambda x: x["tasa"], reverse=True)  # ordenar por tasa
    return simular_pago(deudas, pago_mensual)

def simular_pago(deudas, pago_mensual):
    """Simula el pago de deudas mes a mes"""
    deudas = [d.copy() for d in deudas]  # no modificar original
    meses = 0
    total_intereses = 0
    historial = []

    while any(d["saldo"] > 0 for d in deudas):
        # Aplicar intereses mensuales
        for d in deudas:
            if d["saldo"] > 0:
                interes_mensual = d["saldo"] * (d["tasa"] / 100 / 12)
                d["saldo"] += interes_mensual
                total_intereses += interes_mensual

        # Hacer pagos
        pago_restante = pago_mensual
        for d in deudas:
            if pago_restante <= 0:
                break
            if d["saldo"] > 0:
                pago_a_deuda = min(pago_restante, d["saldo"])
                d["saldo"] -= pago_a_deuda
                pago_restante -= pago_a_deuda

        meses += 1
        if meses > 1000:  # evitar bucle infinito
            break

    return meses, total_intereses

def render():
    st.title("💳 Manejo de Deudas")
    st.markdown("""
    <div style='background-color:#fff8e1; padding:18px; border-radius:12px; margin-bottom:25px; border:1px solid #ffecb3;'>
        <p style='margin:0; color:#e65100; font-size:1.15rem;'>
        📌 Compara dos estrategias para salir de deudas:
        </p>
        <ul style='margin-top:10px; color:#1a1a1a;'>
            <li><strong>Bola de nieve</strong>: Pagas primero la deuda más pequeña (¡motivación rápida!)</li>
            <li><strong>Avalancha</strong>: Pagas primero la deuda con mayor tasa de interés (¡ahorras más!)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Ingreso de deudas
    st.subheader("📝 Ingresa tus deudas")
    
    # Número de deudas
    num_deudas = st.number_input("¿Cuántas deudas tienes?", min_value=1, max_value=10, value=2, step=1)
    
    deudas = []
    for i in range(num_deudas):
        st.markdown(f"#### Deuda {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input(f"Nombre (ej. Tarjeta BBVA)", value=f"Deuda {i+1}", key=f"nombre_{i}")
            saldo = st.number_input(f"Saldo ($)", min_value=0.0, value=5000.0, step=100.0, key=f"saldo_{i}")
        with col2:
            tasa = st.number_input(f"Tasa anual (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0, key=f"tasa_{i}")
            pago_min = st.number_input(f"Pago mínimo ($)", min_value=0.0, value=max(100.0, saldo * 0.02), step=50.0, key=f"pago_min_{i}")
        
        deudas.append({
            "nombre": nombre,
            "saldo": saldo,
            "tasa": tasa,
            "pago_min": pago_min
        })
        st.markdown("---")

    # Pago mensual total
    pago_total = st.number_input(
        "💰 ¿Cuánto puedes pagar **en total** cada mes en deudas?",
        min_value=0.0,
        value=sum(d["pago_min"] for d in deudas) + 500.0,
        step=100.0
    )

    if st.button("🚀 Analizar estrategias", type="primary"):
        if pago_total <= sum(d["pago_min"] for d in deudas):
            st.warning("⚠️ Tu pago mensual debe ser mayor que la suma de los pagos mínimos para salir de deudas.")
        elif any(d["saldo"] <= 0 for d in deudas):
            st.warning("⚠️ Asegúrate de que todas las deudas tengan un saldo mayor a $0.")
        else:
            # Calcular ambas estrategias
            meses_bn, intereses_bn = calcular_pago_bola_nieve(deudas, pago_total)
            meses_av, intereses_av = calcular_pago_avalancha(deudas, pago_total)

            # Mostrar resultados
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📊 Resultados de la comparación")

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    f"""
                    <div class="custom-metric" style="border-left: 5px solid #2a9d8f;">
                        <div class="metric-label">🟢 Bola de Nieve</div>
                        <div class="metric-value" style="color: #2a9d8f;">{meses_bn} meses</div>
                        <div style="font-size: 1rem; color: #555; margin-top: 8px;">
                            Intereses: <b>${intereses_bn:,.0f}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"""
                    <div class="custom-metric" style="border-left: 5px solid #e76f51;">
                        <div class="metric-label">🔴 Avalancha</div>
                        <div class="metric-value" style="color: #e76f51;">{meses_av} meses</div>
                        <div style="font-size: 1rem; color: #555; margin-top: 8px;">
                            Intereses: <b>${intereses_av:,.0f}</b>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Recomendación
            st.markdown("<br>", unsafe_allow_html=True)
            if intereses_av < intereses_bn:
                ahorro = intereses_bn - intereses_av
                st.success(f"✅ **La estrategia Avalancha te ahorraría ${ahorro:,.0f} en intereses** y podría terminar antes.")
                st.info("💡 **Usa esta estrategia si puedes mantenerte disciplinado/a.**")
            else:
                st.success("✅ **Ambas estrategias son similares en este caso.**")
                st.info("💡 **Elige Bola de Nieve si necesitas motivación rápida al ver deudas eliminadas.**")

            # Tabla resumen
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Resumen de tus deudas")
            df_deudas = pd.DataFrame(deudas)
            df_deudas["Tasa anual (%)"] = df_deudas["tasa"]
            df_deudas = df_deudas[["nombre", "saldo", "Tasa anual (%)", "pago_min"]].rename(columns={
                "nombre": "Nombre",
                "saldo": "Saldo ($)",
                "pago_min": "Pago mínimo ($)"
            })
            st.dataframe(df_deudas.style.format({
                "Saldo ($)": "${:,.0f}",
                "Tasa anual (%)": "{:.1f}%",
                "Pago mínimo ($)": "${:,.0f}"
            }), use_container_width=True)

    # Consejo educativo
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Consejo profesional:** Nunca pagues solo el mínimo. Incluso $100 extra al mes pueden reducir años de deuda.")