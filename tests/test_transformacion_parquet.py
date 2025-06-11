import pytest
import pandas as pd
import json
from config import PARQUET_FILE, JSON_FILE

@pytest.fixture(scope="module")
def df_transformado():
    """Carga el DataFrame transformado desde el archivo Parquet una sola vez."""
    assert PARQUET_FILE.exists(), f"❌ No se encontró el archivo: {PARQUET_FILE}"
    return pd.read_parquet(PARQUET_FILE)

@pytest.fixture(scope="module")
def json_original():
    """Carga el JSON original como diccionario una sola vez."""
    with open(JSON_FILE, encoding="utf-8") as f:
        return json.load(f)

def test_columnas_esperadas(df_transformado):
    """Verifica que el Parquet contiene todas las columnas esperadas tras la transformación."""
    columnas_esperadas = [
        "user_id", "full_name", "email", "is_active", "birth_year", "height_cm", "signup_date",
        "roles_csv", "address_full", "mobile_phone", "landline_phone", "newsletter_optin",
        "language", "interests", "project_summary", "comment_status", "has_extra_data",
        "extra_mixed_data"
    ]
    assert set(columnas_esperadas).issubset(df_transformado.columns), \
        "❌ Faltan columnas esperadas en el archivo Parquet"

def test_birth_year(df_transformado, json_original):
    """Comprueba que el año de nacimiento es 2025 - edad."""
    expected = 2025 - json_original["edad"]
    actual = df_transformado.iloc[0]["birth_year"]
    assert actual == expected

def test_altura_transformada(df_transformado, json_original):
    """Verifica que la altura se haya transformado correctamente a centímetros."""
    expected = int(json_original["altura"] * 100)
    actual = df_transformado.iloc[0]["height_cm"]
    assert actual == expected

def test_roles_csv(df_transformado, json_original):
    """Valida que los roles se hayan unido con comas."""
    expected = ",".join(json_original["roles"])
    actual = df_transformado.iloc[0]["roles_csv"]
    assert actual == expected

def test_address_concatenado(df_transformado, json_original):
    """Comprueba que la dirección completa esté formada correctamente."""
    dir = json_original["direccion"]
    expected = f"{dir['calle']}, {dir['codigo_postal']}, {dir['ciudad']}, {dir['pais']}"
    actual = df_transformado.iloc[0]["address_full"]
    assert actual == expected

def test_telefonos(df_transformado, json_original):
    """Revisa que los teléfonos móvil y fijo estén correctamente separados."""
    tel = {t["tipo"]: t["numero"] for t in json_original["telefonos"]}
    fila = df_transformado.iloc[0]
    assert fila["mobile_phone"] == tel.get("móvil")
    assert fila["landline_phone"] == tel.get("fijo")

def test_intereses(df_transformado, json_original):
    """Valida que los intereses se hayan unido con `|`."""
    expected = "|".join(json_original["preferencias"]["temas"])
    actual = df_transformado.iloc[0]["interests"]
    assert actual == expected

def test_project_summary(df_transformado, json_original):
    """Verifica que el resumen de proyectos esté bien formateado."""
    expected = ", ".join(
        [f"{p['nombre']} ({p['progreso']}%)" for p in json_original["proyectos"]]
    )
    actual = df_transformado.iloc[0]["project_summary"]
    assert actual == expected

def test_estado_comentarios(df_transformado, json_original):
    """Comprueba que si comentarios es null, el campo sea 'no_comments'."""
    expected = "no_comments" if json_original["comentarios"] is None else "has_comments"
    actual = df_transformado.iloc[0]["comment_status"]
    assert actual == expected

def test_datos_extra_mixtos(df_transformado, json_original):
    """Valida que el array mixto se haya convertido correctamente a texto plano."""
    valores = json_original["extra"]["array_mixto"]
    expected = ", ".join([str(x).lower() for x in valores])
    actual = df_transformado.iloc[0]["extra_mixed_data"]
    assert actual == expected
