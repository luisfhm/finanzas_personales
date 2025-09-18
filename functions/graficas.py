import plotly.graph_objects as go

def plot_ahorro(df):
    colores = ['#0072B2', '#56B4E9']  # Colores más contrastantes

    fig = go.Figure()

    # Añadir trazas según las columnas disponibles
    if "Ahorro debajo del colchón" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Mes"],
            y=df["Ahorro debajo del colchón"],
            mode='lines+markers',
            name="Debajo del colchón",
            line=dict(color=colores[0], width=4, shape='spline'),
            marker=dict(size=8)
        ))

    if "Poder adquisitivo colchón" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Mes"],
            y=df["Poder adquisitivo colchón"],
            mode='lines+markers',
            name="Poder adquisitivo",
            line=dict(color=colores[1], width=4, shape='spline'),
            marker=dict(size=8)
        ))

    # Configuración de layout con ejes y ticks nítidos
    fig.update_layout(
        xaxis=dict(
            title=dict(text="Mes", font=dict(size=14, color="#2c3e50")),
            tickfont=dict(size=12, color="#2c3e50"),
            showgrid=True,
            gridcolor='rgba(200,200,200,0.3)'
        ),
        yaxis=dict(
            title=dict(text="Ahorro", font=dict(size=14, color="#2c3e50")),
            tickfont=dict(size=12, color="#2c3e50"),
            showgrid=True,
            gridcolor='rgba(200,200,200,0.3)'
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=12, color="#2c3e50"),
        legend=dict(
            borderwidth=0,
            font=dict(size=12, color="#2c3e50")
        )
    )
    # Hover más claro
    fig.update_traces(hovertemplate='%{y:.2f} en %{x}')

    return fig
