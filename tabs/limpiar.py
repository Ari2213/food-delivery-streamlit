import streamlit as st
import pandas as pd


def mostrar(df):
    st.header("2. Limpiar los datos")

    st.markdown("""
    En esta sección evaluamos la calidad del dataset,
    identificando valores faltantes, registros duplicados
    y posibles inconsistencias.
    """)

    # Crear copia para evitar modificar los datos originales
    datos = df.copy()

    # Diagnóstico de calidad
    faltantes = int(datos.isnull().sum().sum())
    duplicados = int(datos.duplicated().sum())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registros originales", len(datos))

    with col2:
        st.metric("Valores faltantes", faltantes)

    with col3:
        st.metric("Filas duplicadas", duplicados)

    # Tabla de valores faltantes
    st.subheader("Valores faltantes por variable")

    tabla_faltantes = pd.DataFrame({
        "Variable": datos.columns,
        "Valores faltantes": datos.isnull().sum().values
    })

    st.dataframe(tabla_faltantes, width="stretch")

    # Limpieza
    st.subheader("Proceso de limpieza")

    datos_limpios = datos.drop_duplicates()

    st.write(
        "Se eliminaron",
        len(datos) - len(datos_limpios),
        "registros duplicados."
    )

    st.metric("Registros después de limpiar", len(datos_limpios))

    st.subheader("Vista previa de los datos limpios")
    st.dataframe(datos_limpios.head(10), width="stretch")

    st.info(
        "La limpieza se realiza sobre una copia del dataset, "
        "sin modificar el archivo CSV original."
    )
    # Validaciones adicionales
    st.subheader("Validaciones de calidad")

    # Pedidos con identificadores repetidos
    ids_duplicados = datos["ID_Pedido"].duplicated().sum()

    # Calificaciones fuera del rango 1 a 5
    calificaciones_invalidas = (
        ~datos["Calificacion"].between(1, 5)
    ).sum()

    # Tiempos de entrega iguales o menores a cero
    tiempos_invalidos = (
        datos["Tiempo_Entrega"] <= 0
    ).sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ID de pedido repetidos", int(ids_duplicados))

    with col2:
        st.metric(
            "Calificaciones fuera de rango",
            int(calificaciones_invalidas)
        )

    with col3:
        st.metric(
            "Tiempos de entrega no positivos",
            int(tiempos_invalidos)
        )