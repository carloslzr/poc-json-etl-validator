import pytest

def test_campos_requeridos(json_data):
    # Comprobar que existen campos que siempre deberían estar
    campos_requeridos = ["id", "nombre", "email", "activo", "fecha_registro"]
    for campo in campos_requeridos:
        assert campo in json_data, f"Falta campo requerido: {campo}"

def test_tipos_de_dato_basicos(json_data):
    # Verificar tipos de datos básicos en campos clave
    assert isinstance(json_data["id"], int), "id debe ser entero"
    assert isinstance(json_data["nombre"], str), "nombre debe ser string"
    assert isinstance(json_data["email"], str), "email debe ser string"
    assert isinstance(json_data["activo"], bool), "activo debe ser booleano"
    assert isinstance(json_data["edad"], int), "edad debe ser entero"
    assert isinstance(json_data["altura"], float), "altura debe ser float"
    assert isinstance(json_data["roles"], list), "roles debe ser lista"
    assert isinstance(json_data["direccion"], dict), "direccion debe ser diccionario"
    assert isinstance(json_data["telefonos"], list), "telefonos debe ser lista"

def test_valores_validos(json_data):
    # Verificar que ciertos valores tienen sentido o están dentro de un rango esperado
    assert 0 < json_data["edad"] < 120, "edad fuera de rango"
    assert 0.5 < json_data["altura"] < 3, "altura fuera de rango"
    assert json_data["activo"] in [True, False], "activo debe ser booleano"

def test_array_roles_no_vacio(json_data):
    # El array roles no debe estar vacío y debe contener solo strings
    roles = json_data["roles"]
    assert roles, "roles no puede estar vacío"
    assert all(isinstance(r, str) for r in roles), "roles debe contener solo strings"

def test_estructura_direccion(json_data):
    # Comprobar campos dentro de un objeto anidado
    direccion = json_data["direccion"]
    campos_direccion = ["calle", "ciudad", "codigo_postal", "pais"]
    for campo in campos_direccion:
        assert campo in direccion, f"Falta campo en direccion: {campo}"
        assert isinstance(direccion[campo], str), f"{campo} en direccion debe ser string"

def test_estructura_telefonos(json_data):
    # Comprobar estructura de array de objetos
    telefonos = json_data["telefonos"]
    assert telefonos, "telefonos no puede estar vacío"
    for tel in telefonos:
        assert "tipo" in tel and "numero" in tel, "telefono debe tener tipo y numero"
        assert isinstance(tel["tipo"], str), "tipo telefono debe ser string"
        assert isinstance(tel["numero"], str), "numero telefono debe ser string"

def test_proyectos_estado_y_progreso(json_data):
    # Validar array de proyectos con campos específicos y lógica de negocio
    proyectos = json_data.get("proyectos", [])
    for proyecto in proyectos:
        assert "nombre" in proyecto and "estado" in proyecto and "progreso" in proyecto
        assert proyecto["estado"] in ["en curso", "completado", "pendiente"]
        progreso = proyecto["progreso"]
        assert isinstance(progreso, (int, float))
        assert 0 <= progreso <= 100, "progreso debe estar entre 0 y 100"

def test_campos_nulos(json_data):
    # Verificar campos que pueden ser null (comentarios, extra.nulo)
    assert "comentarios" in json_data
    assert json_data["comentarios"] is None
    assert "extra" in json_data and "nulo" in json_data["extra"]
    assert json_data["extra"]["nulo"] is None

def test_array_mixto_en_extra(json_data):
    # Validar que el array mixto contenga tipos esperados
    array_mixto = json_data["extra"]["array_mixto"]
    tipos_esperados = (int, str, bool, type(None))
    for elem in array_mixto:
        assert isinstance(elem, tipos_esperados), f"Elemento {elem} de tipo inesperado en array_mixto"

def test_fecha_formato_iso(json_data):
    # Comprobar que fecha_registro cumple formato ISO 8601 (string)
    from datetime import datetime
    fecha = json_data["fecha_registro"]
    try:
        datetime.fromisoformat(fecha.replace("Z", "+00:00"))  # Ajuste para UTC 'Z'
    except ValueError:
        pytest.fail(f"fecha_registro no es un formato ISO 8601 válido: {fecha}")
