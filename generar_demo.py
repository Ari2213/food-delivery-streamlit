
import pandas as pd
import numpy as np
from pathlib import Path

rng = np.random.default_rng(42)
n = 500

segmentos = ["Nuevo", "Frecuente", "VIP", "Inactivo"]
canales = ["Web", "App"]
turnos = ["Mañana", "Tarde", "Noche"]
categorias = ["Pizza", "Hamburguesas", "Comida mexicana", "Ensaladas"]
ciudades = ["Ciudad A", "Ciudad B", "Ciudad C"]
precios = ["Bajo", "Medio", "Alto"]

edad = rng.integers(18, 66, n)
tiempo = rng.integers(15, 81, n)

# Calificaciones ficticias para demostración
calificacion = np.round(
    np.clip(4.5 - 0.025 * (tiempo - 30) + rng.normal(0, 0.6, n), 1, 5),
    1
)

df = pd.DataFrame({
    "ID_Pedido": np.arange(1, n + 1),
    "Fecha": pd.date_range("2025-01-01", periods=n).strftime("%Y-%m-%d"),
    "ID_Cliente": rng.integers(1, 101, n),
    "ID_Restaurante": rng.integers(1, 21, n),
    "Canal": rng.choice(canales, n),
    "Turno": rng.choice(turnos, n),
    "Monto": np.round(rng.uniform(80, 500, n), 2),
    "Descuento": rng.choice([0, 0.05, 0.10, 0.15], n),
    "Tiempo_Entrega": tiempo,
    "Calificacion": calificacion,
    "Edad": edad,
    "Grupo_Edad": pd.cut(
        edad,
        bins=[17, 29, 44, 65],
        labels=["Joven", "Adulto", "Mayor"]
    ).astype(str),
    "Ciudad_Cliente": rng.choice(ciudades, n),
    "Segmento": rng.choice(segmentos, n),
    "Canal_Preferido": rng.choice(canales, n),
    "Nombre_Restaurante": rng.choice(
        [f"Restaurante Demo {i}" for i in range(1, 21)], n
    ),
    "Categoria": rng.choice(categorias, n),
    "Ciudad_Restaurante": rng.choice(ciudades, n),
    "Precio_Nivel": rng.choice(precios, n)
})

df["Calificacion_Baja"] = (df["Calificacion"] <= 3).astype(int)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/food_delivery_demo.csv", index=False, encoding="utf-8-sig")

print("Dataset de demostración generado:", len(df), "registros")
print("Calificaciones bajas:", df["Calificacion_Baja"].sum())
