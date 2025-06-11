import os
import json
from genson import SchemaBuilder

# Solicitar al usuario la ruta del archivo JSON
ruta_json = input("📄 Introduce la ruta al JSON de entrada (ej.: data/datos.json): ").strip()

# Comprobar que el archivo existe
if not os.path.isfile(ruta_json):
    print(f"❌ El archivo '{ruta_json}' no existe.")
    exit(1)

# Solicitar los campos requeridos
campos_required = input("🔑 Introduce los campos 'required' separados por comas: ").strip()
required_fields = [campo.strip() for campo in campos_required.split(",") if campo.strip()]

# Cargar el JSON
with open(ruta_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Generar el esquema
builder = SchemaBuilder()
builder.add_object(data)
schema = builder.to_schema()

# Añadir $schema (versión de JSON Schema que se usará)
schema["$schema"] = "http://json-schema.org/draft-07/schema#"

# Añadir los campos 'required' si se proporcionaron
if required_fields:
    schema["required"] = required_fields

# Generar nombre para el archivo de salida en la misma ruta
nombre_salida = os.path.splitext(ruta_json)[0] + "_schema.json"

# Verificar si el archivo ya existe
if os.path.exists(nombre_salida):
    respuesta = input(f"⚠️ El archivo '{nombre_salida}' ya existe. ¿Deseas sobrescribirlo? (s/n): ").strip().lower()
    if respuesta != "s":
        print("🚫 Operación cancelada. No se sobrescribió el archivo.")
        exit(0)

# Guardar el schema
with open(nombre_salida, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2)

print(f"✅ Esquema guardado en: {nombre_salida}")
