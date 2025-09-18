# functions/graficas.py
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
def plot_ahorro(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    columnas_labels = {
        "Ahorro debajo del colchón": "Debajo del colchón",
        "Poder adquisitivo colchón": "Poder adquisitivo",
        "Ahorro con inversión": "Inversión"
    }

    for col, label in columnas_labels.items():
        if col in df.columns:
            ax.plot(df["Mes"], df[col], label=label)

    # Formato de eje Y en pesos
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad")
    ax.set_title("Evolución del ahorro")
    ax.legend()
    ax.grid(True)
    return fig
