
import streamlit as st
import pandas as pd


def mostrar(df):
    st.header("1. Entender los datos")

    st.markdown("""
    **Pregunta inicial:**

    ¿Qué factores se relacionan con las calificaciones
    bajas en los pedidos de Food Delivery?
    """)

    # Indicadores principales
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de pedidos", len(df))

    with col2:
        st.metric("Número de variables", len(df.columns))

    with col3:
        st.metric(
            "Calificaciones bajas",
            int(df["Calificacion_Baja"].sum())
        )

    # Vista previa
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head(10), width="stretch")

    # Tipos de variables
    st.subheader("Tipos de variables")

    tipos = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": df.dtypes.astype(str).values
    })

    st.dataframe(tipos, width="stretch")

    # Diagnóstico inicial
    st.subheader("Diagnóstico del dataset")

    diagnostico = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": df.dtypes.astype(str).values,
        "Valores únicos": df.nunique().values,
        "Valores faltantes": df.isnull().sum().values
    })

    st.dataframe(diagnostico, width="stretch")

    # Registros duplicados
    st.subheader("Problemas potenciales")

    duplicados = df.duplicated().sum()

    st.metric(
        "Registros duplicados",
        int(duplicados)
    )

    # Exploración de variables
    st.subheader("Explorar una variable")

    variable = st.selectbox(
        "Selecciona una variable:",
        df.columns
    )

    if pd.api.types.is_numeric_dtype(df[variable]):
        st.write("Variable numérica")
        st.dataframe(
            df[variable].describe().to_frame(),
            width="stretch"
        )
    else:
        st.write("Variable categórica")

        frecuencias = df[variable].value_counts()

        st.dataframe(
            frecuencias.rename("Frecuencia").to_frame(),
            width="stretch"
        )
