
import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def mostrar(df):
    st.header("4. Estadística predictiva")

    st.write(
        "Entrenaremos un modelo de regresión logística "
        "para identificar pedidos con riesgo de "
        "recibir una calificación baja."
    )

    # Variables disponibles antes de completar la entrega
    numericas = ["Monto", "Descuento", "Edad"]

    categoricas = [
        "Canal",
        "Turno",
        "Segmento",
        "Categoria",
        "Precio_Nivel",
        "Ciudad_Cliente",
        "Ciudad_Restaurante"
    ]

    X = df[numericas + categoricas]
    y = df["Calificacion_Baja"]

    # Dividir los datos: 80 % entrenamiento y 20 % prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Preparar los datos
    preprocesamiento = ColumnTransformer([
        ("numericas", StandardScaler(), numericas),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), categoricas)
    ])

    # Crear el modelo
    modelo = Pipeline([
        ("preprocesamiento", preprocesamiento),
        ("clasificador", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    # Entrenar el modelo
    modelo.fit(X_train, y_train)

    # Evaluar con datos que no se utilizaron para entrenar
    predicciones = modelo.predict(X_test)

    

    exactitud = accuracy_score(y_test, predicciones)
    precision = precision_score(y_test, predicciones, zero_division=0)
    recall = recall_score(y_test, predicciones, zero_division=0)
    f1 = f1_score(y_test, predicciones, zero_division=0)

    st.subheader("Resultados del modelo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Exactitud", f"{exactitud:.2%}")
    col2.metric("Precisión", f"{precision:.2%}")
    col3.metric("Recall", f"{recall:.2%}")
    col4.metric("F1-score", f"{f1:.2%}")

    st.subheader("Matriz de confusión")

    matriz = confusion_matrix(
        y_test,
        predicciones,
        labels=[0, 1]
    )

    matriz_df = pd.DataFrame(
        matriz,
        index=["Real favorable", "Real baja"],
        columns=["Predicha favorable", "Predicha baja"]
    )

    st.dataframe(matriz_df, width="stretch")

    st.subheader("Reporte de clasificación")

    reporte = classification_report(
        y_test,
        predicciones,
        zero_division=0
    )

    st.code(reporte)

    st.info(
        "El modelo utiliza información previa a la entrega. "
        "Sus predicciones representan estimaciones estadísticas "
        "y no garantizan la satisfacción de cada cliente."
    )
