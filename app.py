import streamlit as st
import pandas as pd
from tabs import entender, limpiar, descriptiva, predictiva, prescriptiva, decisiones
from pathlib import Path

# Configuración general
st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide"
)

# Título
st.title("🍔 Food Delivery Analytics")

st.markdown("""
Sistema de análisis de datos y predicción de satisfacción
en servicios de entrega de alimentos.
""")

@st.cache_data
def cargar_datos():
    archivo_original = Path("data/food_delivery.csv")
    archivo_demo = Path("data/food_delivery_demo.csv")

    if archivo_original.exists():
        return pd.read_csv(archivo_original), False

    return pd.read_csv(archivo_demo), True


df, modo_demo = cargar_datos()

if modo_demo:
    st.warning(
        "Modo demostración: se utilizan 500 pedidos "
        "completamente sintéticos. Los resultados "
        "no corresponden al análisis original."
    )

# Crear seis pestañas
tabs = st.tabs([
    "1. Entender",
    "2. Limpiar",
    "3. Describir",
    "4. Predecir",
    "5. Prescribir",
    "6. Decidir"
])

# Primera pestaña
with tabs[0]:
    entender.mostrar(df)

# Otras pestañas
with tabs[1]:
    limpiar.mostrar(df)

with tabs[2]:
    descriptiva.mostrar(df)
    
with tabs[3]:
    predictiva.mostrar(df)

with tabs[4]:
    prescriptiva.mostrar(df)

with tabs[5]:
    decisiones.mostrar(df)