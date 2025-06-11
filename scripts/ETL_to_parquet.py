import json
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# Ruta de entrada y salida
ruta_json = input("📄 Introduce la ruta al JSON de entrada (ej.: data/datos.json): ").strip()
ruta_parquet = Path("data/resultado_transformado.parquet")

# Comprobar que el archivo existe
if not os.path.isfile(ruta_json):
    print(f"❌ El archivo '{ruta_json}' no existe.")
    exit(1)

# Leer el JSON
with open(ruta_json, encoding="utf-8") as f:
    raw = json.load(f)

# Reglas de transformación simuladas
data = {
    "user_id": raw.get("id"),
    "full_name": raw.get("nombre"),
    "email": raw.get("email"),
    "is_active": raw.get("activo", False),
    "birth_year": 2025 - raw.get("edad", 0),
    "height_cm": int(raw.get("altura", 0) * 100),
    "signup_date": raw.get("fecha_registro"),
    "roles_csv": ",".join(raw.get("roles", [])),
    "address_full": f"{raw['direccion']['calle']}, {raw['direccion']['codigo_postal']}, {raw['direccion']['ciudad']}, {raw['direccion']['pais']}",
    "mobile_phone": next((t["numero"] for t in raw.get("telefonos", []) if t["tipo"] == "móvil"), None),
    "landline_phone": next((t["numero"] for t in raw.get("telefonos", []) if t["tipo"] == "fijo"), None),
    "newsletter_optin": raw.get("preferencias", {}).get("newsletter"),
    "language": raw.get("preferencias", {}).get("idioma"),
    "interests": "|".join(raw.get("preferencias", {}).get("temas", [])),
    "project_summary": ", ".join([
        f"{p['nombre']} ({p['progreso']}%)" for p in raw.get("proyectos", [])
    ]),
    "comment_status": "no_comments" if raw.get("comentarios") is None else "has_comments",
    "has_extra_data": raw.get("extra") is not None,
    "extra_mixed_data": ", ".join([str(x).lower() for x in raw.get("extra", {}).get("array_mixto", [])]),
}

# Verificar si el archivo ya existe
if os.path.exists(ruta_parquet):
    respuesta = input(f"⚠️ El archivo '{ruta_parquet}' ya existe. ¿Deseas sobrescribirlo? (s/n): ").strip().lower()
    if respuesta != "s":
        print("🚫 Operación cancelada. No se sobrescribió el archivo.")
        exit(0)

# Crear DataFrame y guardar como Parquet
df = pd.DataFrame([data])
table = pa.Table.from_pandas(df)
pq.write_table(table, ruta_parquet)

print(f"✅ Fichero Parquet generado: {ruta_parquet}")




