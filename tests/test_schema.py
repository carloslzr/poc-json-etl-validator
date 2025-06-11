import json
import pytest
from jsonschema import Draft7Validator
from config import SCHEMA_FILE

def test_validacion_schema(json_data):
    ruta_schema = SCHEMA_FILE

    if not ruta_schema.is_file():
        pytest.exit(f"❌ El archivo schema '{ruta_schema}' no existe. Verifica SCHEMA_FILE en config.py")

    with ruta_schema.open(encoding="utf-8") as f:
        schema = json.load(f)

    validator = Draft7Validator(schema)
    errores = sorted(validator.iter_errors(json_data), key=lambda e: e.path)

    if errores:
        for error in errores:
            ruta_error = " → ".join(str(p) for p in error.path)
            print(f"❌ Error: {error.message} en {ruta_error}")
        pytest.fail(f"Se encontraron {len(errores)} errores de validación en el JSON.")
    else:
        print("✅ El JSON cumple con el esquema.")
