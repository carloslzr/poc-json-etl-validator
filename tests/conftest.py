import pytest
import json
from config import JSON_FILE

@pytest.fixture(scope="session")
def json_data(request):
    ruta_json = JSON_FILE

    if not ruta_json.is_file():
        pytest.exit(f"❌ El archivo JSON '{ruta_json}' no existe. Verifica JSON_FILE en config.py")

    with ruta_json.open(encoding="utf-8") as f:
        contenido = json.load(f)

    request.session.json_filename = ruta_json.name  # sólo el nombre del archivo
    return contenido
