import pandas as pd
from pathlib import Path

# Rutas
CARPETA_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_EXCEL = CARPETA_PROYECTO / "FoodDelivery_Modelo_2025.xlsx"
ARCHIVO_CSV = CARPETA_PROYECTO / "data" / "food_delivery.csv"

# Leer las tres hojas
pedidos = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Pedidos")
clientes = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Clientes")
restaurantes = pd.read_excel(ARCHIVO_EXCEL, sheet_name="Restaurantes")

# Eliminar nombres de personas
clientes = clientes.drop(columns=["Nombre_Cliente"], errors="ignore")

# Evitar columnas de ciudad duplicadas
clientes = clientes.rename(columns={"Ciudad": "Ciudad_Cliente"})
restaurantes = restaurantes.rename(columns={"Ciudad": "Ciudad_Restaurante"})

# Evitar confundir el nombre del restaurante con el del cliente
restaurantes = restaurantes.rename(columns={"Nombre": "Nombre_Restaurante"})

# Combinar información
datos = pedidos.merge(clientes, on="ID_Cliente", how="left")
datos = datos.merge(restaurantes, on="ID_Restaurante", how="left")

# Crear variable objetivo
# 1 = calificación baja (1, 2 o 3)
# 0 = calificación favorable (4 o 5)
datos["Calificacion_Baja"] = (
    datos["Calificacion"] <= 3
).astype(int)

# Crear carpeta de salida si no existe
ARCHIVO_CSV.parent.mkdir(parents=True, exist_ok=True)

# Guardar dataset
datos.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8-sig")

# Mostrar resultados
print("Dataset preparado correctamente")
print("Registros:", len(datos))
print("Variables:", len(datos.columns))
print("Calificaciones bajas:", datos["Calificacion_Baja"].sum())
print("Valores faltantes:", datos.isnull().sum().sum())
print("Archivo guardado en:", ARCHIVO_CSV) 