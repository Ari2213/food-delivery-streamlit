
import pandas as pd
import numpy as np
from pathlib import Path

# Configuración
CANTIDAD = 5000
SEMILLA = 42

rng = np.random.default_rng(SEMILLA)

registros = []

for i in range(CANTIDAD):

    id_pedido = 7989 + i

    fecha = (
        pd.Timestamp("2025-01-01")
        + pd.Timedelta(days=int(rng.integers(0, 365)))
    )

    id_cliente = int(rng.integers(1, 91))
    id_restaurante = int(rng.integers(1, 21))

    canal = rng.choice(["Web", "App"])
    turno = rng.choice(["Mañana", "Tarde", "Noche"])

    monto = round(float(rng.uniform(80, 500)), 2)
    descuento = int(rng.choice([0, 5, 10, 15, 20]))

    tiempo_entrega = int(
        np.clip(rng.normal(43, 14), 15, 90)
    )

    # Simulamos mayor riesgo de insatisfacción
    # cuando el tiempo de entrega aumenta.
    probabilidad_baja = np.clip(
        0.35 + (tiempo_entrega - 35) * 0.012,
        0.10,
        0.85
    )

    es_baja = rng.random() < probabilidad_baja

    if es_baja:
        calificacion = round(float(rng.uniform(1.5, 3.0)), 1)
    else:
        calificacion = round(float(rng.uniform(3.1, 5.0)), 1)

    registros.append({
        "ID_Pedido": id_pedido,
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "ID_Cliente": id_cliente,
        "ID_Restaurante": id_restaurante,
        "Canal": canal,
        "Turno": turno,
        "Monto": monto,
        "Descuento": descuento,
        "Tiempo_Entrega": tiempo_entrega,
        "Calificacion": calificacion
    })

df = pd.DataFrame(registros)

# Guardar por separado del dataset original
Path("data").mkdir(exist_ok=True)

ruta = "data/pedidos_sinteticos_5000.csv"

df.to_csv(ruta, index=False, encoding="utf-8-sig")

print("Archivo generado:", ruta)
print("Total de registros:", len(df))
print("Calificaciones bajas:", (df["Calificacion"] <= 3).sum())
print("Calificaciones favorables:", (df["Calificacion"] > 3).sum())
print(df.head())
