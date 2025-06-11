from pathlib import Path

# Base path del proyecto (directorio donde está config.py)
BASE_DIR = Path(__file__).parent.parent.resolve()

# Rutas absolutas a los archivos JSON y schema
JSON_FILE = BASE_DIR / "data" / "datos.json"
SCHEMA_FILE = BASE_DIR / "data" / "datos_schema.json"

PARQUET_FILE = BASE_DIR / "data" / "resultado_transformado.parquet"
