# functions/datos.py
import requests
import pandas as pd
from datetime import datetime
import streamlit as st

@st.cache_data(ttl=3600)  # Caché por 1 hora
def obtener_inflacion_mx():
    """
    Obtiene la inflación anual más reciente de México desde la API de Banxico.
    Retorna: (fecha_str, valor_inflacion) o (None, None) si falla.
    """
    url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP68257/datos/oportuno"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extraer el último dato
        ultimo_dato = data["bmx"]["series"][0]["datos"][-1]
        fecha = ultimo_dato["fecha"]  # formato: "01/03/2025"
        valor = float(ultimo_dato["dato"])
        
        # Convertir fecha a "marzo 2025"
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        fecha_str = fecha_dt.strftime("%B %Y").capitalize()
        
        return fecha_str, valor
    except Exception as e:
        # Fallback: intentar cargar desde CSV local
        try:
            df = pd.read_csv("data/inflacion_mx.csv")
            df["fecha"] = pd.to_datetime(df["fecha"])
            df = df.sort_values("fecha")
            ultima_fecha = df.iloc[-1]["fecha"]
            valor = df.iloc[-1]["inflacion_anual"]
            fecha_str = ultima_fecha.strftime("%B %Y").capitalize()
            return fecha_str, valor
        except:
            return None, None