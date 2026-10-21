
import streamlit as st
import pandas as pd


def mostrar(df):
    st.header("6. Toma de decisiones")

    st.markdown("""
    En esta sección utilizamos los resultados del análisis
    para identificar áreas de atención y seleccionar
    posibles acciones de mejora.
    """)

    # Indicadores generales
    porcentaje_bajas = df["Calificacion_Baja"].mean() * 100
    tiempo_promedio = df["Tiempo_Entrega"].mean()

    col1, col2 = st.columns(2)

    col1.metric(
        "Porcentaje de calificaciones bajas",
        f"{porcentaje_bajas:.2f}%"
    )

    col2.metric(
        "Tiempo promedio de entrega",
        f"{tiempo_promedio:.1f} minutos"
    )

    # Comparación por segmento
    st.subheader("Identificación de segmentos prioritarios")

    resumen = (
        df.groupby("Segmento")
        .agg(
            Pedidos=("Calificacion_Baja", "count"),
            Calificaciones_Bajas=("Calificacion_Baja", "sum"),
            Tiempo_Promedio=("Tiempo_Entrega", "mean")
        )
        .reset_index()
    )

    resumen["Porcentaje_Bajas"] = (
        resumen["Calificaciones_Bajas"]
        / resumen["Pedidos"] * 100
    )

    resumen = resumen.sort_values(
        "Porcentaje_Bajas",
        ascending=False
    )

    st.dataframe(
        resumen.style.format({
            "Tiempo_Promedio": "{:.1f}",
            "Porcentaje_Bajas": "{:.2f}%"
        }),
        width="stretch"
    )

    # Selección de una acción
    st.subheader("Seleccionar una acción de mejora")

    accion = st.selectbox(
        "¿Qué acción deseas evaluar?",
        [
            "Reducir tiempos de entrega",
            "Mejorar la comunicación con los clientes",
            "Dar seguimiento a calificaciones bajas"
        ]
    )

    if accion == "Reducir tiempos de entrega":
        st.info(
            "Propuesta: revisar los pedidos con mayores "
            "tiempos de entrega e identificar oportunidades "
            "para optimizar el servicio."
        )

    elif accion == "Mejorar la comunicación con los clientes":
        st.info(
            "Propuesta: informar sobre retrasos y ofrecer "
            "actualizaciones oportunas del estado del pedido."
        )

    else:
        st.info(
            "Propuesta: analizar los pedidos con calificaciones "
            "bajas y registrar los problemas reportados "
            "para identificar patrones recurrentes."
        )

    # Decisión basada en datos
    st.subheader("Decisión sugerida")

    if not resumen.empty:
        segmento_prioritario = resumen.iloc[0]["Segmento"]

        st.success(
            f"Se recomienda comenzar revisando el segmento "
            f"'{segmento_prioritario}', ya que presenta "
            f"la mayor proporción observada de "
            f"calificaciones bajas."
        )

    st.warning(
        "Las decisiones propuestas deben validarse antes "
        "de implementarse. Los resultados descriptivos "
        "no demuestran causalidad y el modelo predictivo "
        "presenta limitaciones de precisión."
    )
