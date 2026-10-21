
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score
)

# 1. Cargar los archivos
original = pd.read_csv("data/food_delivery.csv")
sinteticos = pd.read_csv("data/pedidos_sinteticos_5000.csv")

numericas = ["Monto", "Descuento", "Edad"]
categoricas = [
    "Canal", "Turno", "Segmento", "Categoria",
    "Precio_Nivel", "Ciudad_Cliente", "Ciudad_Restaurante"
]
variables = numericas + categoricas

# 2. Separar los pedidos originales
train, test = train_test_split(
    original,
    test_size=0.20,
    random_state=42,
    stratify=original["Calificacion_Baja"]
)

# 3. Completar datos de clientes y restaurantes
# usando los registros originales de entrenamiento
clientes = train.drop_duplicates("ID_Cliente")[
    ["ID_Cliente", "Edad", "Segmento", "Ciudad_Cliente"]
]

restaurantes = train.drop_duplicates("ID_Restaurante")[
    ["ID_Restaurante", "Categoria", "Precio_Nivel",
     "Ciudad_Restaurante"]
]

sinteticos = sinteticos.merge(
    clientes, on="ID_Cliente", how="left"
)
sinteticos = sinteticos.merge(
    restaurantes, on="ID_Restaurante", how="left"
)

# Asegurar que el descuento sea numérico
sinteticos["Descuento"] = (
    sinteticos["Descuento"]
    .astype(str)
    .str.replace("%", "", regex=False)
)
sinteticos["Descuento"] = pd.to_numeric(
    sinteticos["Descuento"], errors="coerce"
)

# Convertir porcentajes a la misma escala que el original
if original["Descuento"].max() <= 1:
    sinteticos["Descuento"] /= 100

# Crear variable objetivo
sinteticos["Calificacion_Baja"] = (
    sinteticos["Calificacion"] <= 3
).astype(int)

# Eliminar registros sin información suficiente
sinteticos = sinteticos.dropna(
    subset=variables + ["Calificacion_Baja"]
)

print("Registros sintéticos utilizables:", len(sinteticos))

def crear_modelo():
    preprocesamiento = ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categoricas)
    ])

    return Pipeline([
        ("preprocesamiento", preprocesamiento),
        ("clasificador", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

def evaluar(nombre, entrenamiento):
    modelo = crear_modelo()

    modelo.fit(
        entrenamiento[variables],
        entrenamiento["Calificacion_Baja"]
    )

    pred = modelo.predict(test[variables])

    return {
        "Modelo": nombre,
        "Exactitud": accuracy_score(test["Calificacion_Baja"], pred),
        "Precisión": precision_score(
            test["Calificacion_Baja"], pred, zero_division=0
        ),
        "Recall": recall_score(
            test["Calificacion_Baja"], pred, zero_division=0
        ),
        "F1-score": f1_score(
            test["Calificacion_Baja"], pred, zero_division=0
        )
    }

# 4. Comparar los experimentos
resultado_original = evaluar("Solo originales", train)

train_ampliado = pd.concat(
    [train, sinteticos],
    ignore_index=True
)

resultado_sintetico = evaluar(
    "Originales + 5000 sintéticos",
    train_ampliado
)

resultados = pd.DataFrame([
    resultado_original,
    resultado_sintetico
])

print("\nCOMPARACIÓN DE MODELOS\n")
print(resultados.to_string(
    index=False,
    formatters={
        "Exactitud": "{:.2%}".format,
        "Precisión": "{:.2%}".format,
        "Recall": "{:.2%}".format,
        "F1-score": "{:.2%}".format
    }
))
