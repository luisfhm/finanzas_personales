# functions/graficas.py
import matplotlib.pyplot as plt

def plot_ahorro(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Lista de columnas que queremos graficar y sus etiquetas
    columnas_labels = {
        "Ahorro debajo del colchón": "Debajo del colchón",
        "Poder adquisitivo colchón": "Poder adquisitivo",
        "Ahorro con inversión": "Inversión"
    }

    # Graficar solo las columnas que existan en df
    for col, label in columnas_labels.items():
        if col in df.columns:
            ax.plot(df["Mes"], df[col], label=label)

    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad")
    ax.set_title("Evolución del ahorro")
    ax.legend()
    ax.grid(True)
    
    return fig
