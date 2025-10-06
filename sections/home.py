import streamlit as st

def render():
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
            st.rerun()

    # Filosofía
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