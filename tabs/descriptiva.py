
import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar(df):
    st.header("3. Estadística descriptiva")

    st.markdown("""
    En esta sección analizamos las características de los
    pedidos y su relación con la satisfacción del cliente.
    """)

    # Indicadores principales
    porcentaje_bajas = df["Calificacion_Baja"].mean() * 100
    tiempo_promedio = df["Tiempo_Entrega"].mean()
    monto_promedio = df["Monto"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Calificaciones bajas",
            f"{porcentaje_bajas:.2f}%"
        )

    with col2:
        st.metric(
            "Tiempo promedio de entrega",
            f"{tiempo_promedio:.1f} min"
        )

    with col3:
        st.metric(
            "Monto promedio del pedido",
            f"${monto_promedio:.2f}"
        )

    # Gráfica de calificaciones
    st.subheader("Distribución de calificaciones")

    conteo = (
        df["Calificacion"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    conteo.columns = ["Calificación", "Pedidos"]

    fig1 = px.bar(
        conteo,
        x="Calificación",
        y="Pedidos",
        title="Número de pedidos por calificación"
    )

    st.plotly_chart(fig1, width="stretch")

    # Relación entre entrega y satisfacción
    st.subheader("Tiempo de entrega y satisfacción")

    resumen = (
        df.groupby("Calificacion_Baja")["Tiempo_Entrega"]
        .mean()
        .reset_index()
    )

    resumen["Satisfacción"] = resumen[
        "Calificacion_Baja"
    ].map({
        0: "Calificación favorable",
        1: "Calificación baja"
    })

    fig2 = px.bar(
        resumen,
        x="Satisfacción",
        y="Tiempo_Entrega",
        title="Tiempo promedio según la satisfacción",
        labels={"Tiempo_Entrega": "Minutos"}
    )

    st.plotly_chart(fig2, width="stretch")

    st.info(
        "Estas gráficas muestran asociaciones descriptivas. "
        "No demuestran que el tiempo de entrega sea la causa "
        "de una calificación baja."
    )
