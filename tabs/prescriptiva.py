import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar(df):
    st.header("5. Estadística prescriptiva")

    st.markdown("""
    En esta sección proponemos acciones para mejorar
    la satisfacción de los clientes a partir de los
    resultados del análisis descriptivo y predictivo.
    """)

    # Comparar tiempos de entrega según la satisfacción
    resumen = (
        df.groupby("Calificacion_Baja")["Tiempo_Entrega"]
        .agg(["mean", "count"])
        .reset_index()
    )

    resumen["Satisfacción"] = resumen["Calificacion_Baja"].map({
        0: "Favorable",
        1: "Baja"
    })

    st.subheader("Tiempo de entrega y satisfacción")

    fig = px.bar(
        resumen,
        x="Satisfacción",
        y="mean",
        color="Satisfacción",
        title="Tiempo promedio de entrega según la calificación",
        labels={"mean": "Tiempo promedio (minutos)"}
    )

    st.plotly_chart(fig, width="stretch")

    # Recomendaciones basadas en los hallazgos
    st.subheader("Recomendaciones de mejora")

    st.markdown("""
    **1. Revisar los tiempos de entrega**

    Los pedidos con calificaciones bajas presentan,
    en promedio, tiempos de entrega mayores.
    Se recomienda identificar las causas de los retrasos.

    **2. Mejorar la comunicación con los clientes**

    Informar oportunamente cuando exista un retraso
    y proporcionar actualizaciones del pedido.

    **3. Analizar los pedidos con calificaciones bajas**

    Revisar los casos de insatisfacción para identificar
    posibles problemas recurrentes.

    **4. Evaluar las acciones implementadas**

    Comparar periódicamente los tiempos de entrega
    y el porcentaje de calificaciones bajas.
    """)

    st.subheader("Recomendaciones por segmento")

    segmento = st.selectbox(
        "Selecciona un segmento de clientes:",
        sorted(df["Segmento"].dropna().unique())
    )

    datos_segmento = df[df["Segmento"] == segmento]

    porcentaje_bajas = (
        datos_segmento["Calificacion_Baja"].mean() * 100
    )

    tiempo_promedio = datos_segmento["Tiempo_Entrega"].mean()

    col1, col2 = st.columns(2)

    col1.metric(
        "Calificaciones bajas del segmento",
        f"{porcentaje_bajas:.2f}%"
    )

    col2.metric(
        "Tiempo promedio de entrega",
        f"{tiempo_promedio:.1f} min"
    )

    if porcentaje_bajas > df["Calificacion_Baja"].mean() * 100:
        st.warning(
            "Este segmento presenta una proporción de "
            "calificaciones bajas superior al promedio general. "
            "Se recomienda revisar sus pedidos y detectar "
            "posibles problemas en el servicio."
        )
    else:
        st.success(
            "Este segmento presenta una proporción de "
            "calificaciones bajas igual o inferior al "
            "promedio general. Se recomienda mantener "
            "el seguimiento de su satisfacción."
        )

    st.caption(
        "Las recomendaciones se basan en asociaciones "
        "observadas en los datos. No demuestran causalidad "
        "ni garantizan una mejora en la satisfacción."
    )
