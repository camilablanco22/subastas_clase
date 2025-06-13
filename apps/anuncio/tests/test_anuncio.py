from decimal import Decimal

import pytest
import pytest
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client, get_intruso
from .fixtures_anuncio import get_anuncio
from .fixtures_categoria import get_categoria
from ..models import Anuncio

@pytest.mark.django_db
def test_api_creacion_anuncio(get_authenticated_client, get_anuncio, get_categoria, get_user_generico):
    client = get_authenticated_client
    categoria = get_categoria
    data = {
            "titulo": "Vestido de gala",
            "descripcion": "Vestido rojo largo de gala, tela satinada.",
            "precio_inicial": "15000.00",
            "categorias": [
                categoria.id
            ],
            "fecha_inicio": "2025-06-20T17:01:00Z",
            "fecha_fin": "2025-06-30T17:01:00Z"
    }

    response = client.post(f'/api/v3/anuncio/', data=data)
    assert response.status_code == 201
    assert Anuncio.objects.filter(titulo='Vestido de gala').count() == 1

    anuncio = Anuncio.objects.get(titulo='Vestido de gala')
    assert anuncio.descripcion == data["descripcion"]
    assert anuncio.precio_inicial == Decimal(data["precio_inicial"])
    assert anuncio.fecha_inicio.date().isoformat() == data["fecha_inicio"][:10]
    assert anuncio.publicado_por == get_user_generico

#Comprobamos las validaciones de campos especificos. (validate_[campo])
@pytest.mark.django_db
@pytest.mark.parametrize("field, value, expected_error", [
    ("precio_inicial", "0.00", "mayor o igual a cero"),
    ("fecha_inicio", "2025-06-01T00:00:00Z", "La fecha de inicio no puede ser anterior a la fecha actual."),
    ("fecha_inicio", "2025-07-01T00:00:00Z", "La subasta no puede tardar mas de 15 días en iniciar."),
])
#Comprobamos las validaciones de campos especificos.
def test_anuncio_campo_invalido(get_authenticated_client, get_categoria, field, value, expected_error):
    client = get_authenticated_client
    categoria = get_categoria

    data = {
        "titulo": "Vestido de gala",
        "descripcion": "Vestido rojo largo de gala, tela satinada.",
        "precio_inicial": "15000.00",
        "categorias": [
            categoria.id
        ],
        "fecha_inicio": "2025-06-20T17:01:00Z",
        "fecha_fin": "2025-06-30T17:01:00Z",
        field: value}

    response = client.post('/api/v3/anuncio/', data=data, format='json')

    assert response.status_code == 400
    assert field in response.data
    assert expected_error.lower() in str(response.data[field][0]).lower()

#Comprobamos las validaciones hechas en validate (implican mas de un campo)
@pytest.mark.django_db
@pytest.mark.parametrize("override_data, expected_error", [
    (
        {"fecha_inicio": "2025-06-20T17:01:00Z", "fecha_fin": "2025-06-19T17:01:00Z"},
        "debe ser posterior a la fecha de inicio"
    ),
    (
        {"fecha_inicio": "2025-06-20T17:01:00Z", "fecha_fin": "2026-06-21T17:01:00Z"},
        "no puede durar mas de un año"
    ),
])
#Comprobamos las validaciones hechas en validate (implican mas de un campo)
def test_anuncio_errores_generales(get_authenticated_client, get_categoria, override_data, expected_error):
    client = get_authenticated_client
    categoria = get_categoria

    data = {
        "titulo": "Vestido inválido",
        "descripcion": "Con errores generales.",
        "precio_inicial": "15000.00",
        "categorias": [categoria.id],
        "fecha_inicio": "2025-06-20T17:01:00Z",
        "fecha_fin": "2025-06-30T17:01:00Z"
    }

    data.update(override_data)

    response = client.post("/api/v3/anuncio/", data=data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert expected_error.lower() in str(response.data["non_field_errors"][0]).lower()


@pytest.mark.django_db
def test_modificacion_correcta_anuncio(get_authenticated_client, get_anuncio, get_categoria, get_user_generico):
    client = get_authenticated_client
    anuncio = get_anuncio
    categoria = get_categoria
    usuario = get_user_generico

    nuevos_datos = {
        "titulo": "Título actualizado",
        "descripcion": "Descripción actualizada",
        "precio_inicial": "20000.00",
        "fecha_inicio": "2025-06-16T12:00:00Z",
        "fecha_fin": "2025-06-21T12:00:00Z",
        "categorias": [categoria.id]
    }

    response = client.put(f"/api/v3/anuncio/{anuncio.id}/", data=nuevos_datos, format="json")

    assert response.status_code == 200

    nuevo_anuncio = Anuncio.objects.get(id=anuncio.id) #SE PUEDE USAR anuncio.refresh_from_db()

    assert nuevo_anuncio.titulo == nuevos_datos["titulo"]
    assert nuevo_anuncio.descripcion == nuevos_datos["descripcion"]
    assert nuevo_anuncio.precio_inicial == Decimal(nuevos_datos["precio_inicial"])
    assert nuevo_anuncio.fecha_inicio.isoformat()[:10] == nuevos_datos["fecha_inicio"][:10]
    assert nuevo_anuncio.fecha_fin.isoformat()[:10] == nuevos_datos["fecha_fin"][:10]
    assert nuevo_anuncio.publicado_por == usuario


@pytest.mark.django_db
@pytest.mark.parametrize("field, value, expected_error", [
    ("precio_inicial", "0.00", "mayor o igual a cero"),
    ("fecha_inicio", "2024-06-01T00:00:00Z", "fecha de inicio no puede ser anterior"),
    ("fecha_inicio", "2025-08-01T00:00:00Z", "tardar mas de 15 días en iniciar"),
])
def test_modificar_anuncio_campo_invalido(get_authenticated_client, get_anuncio, get_categoria, field, value, expected_error):
    client = get_authenticated_client
    anuncio = get_anuncio
    categoria = get_categoria

    nuevos_datos = {
        "titulo": "Título actualizado",
        "descripcion": "Descripción actualizada",
        "precio_inicial": "20000.00",
        "fecha_inicio": "2025-06-16T12:00:00Z",
        "fecha_fin": "2025-06-21T12:00:00Z",
        "categorias": [categoria.id],
        field: value
    }


    response = client.put(f"/api/v3/anuncio/{anuncio.id}/", data=nuevos_datos, format="json")

    assert response.status_code == 400
    assert field in response.data
    assert expected_error.lower() in str(response.data[field][0]).lower()


@pytest.mark.django_db
@pytest.mark.parametrize("override_data, expected_error", [
    (
        {"fecha_inicio": "2025-06-20T17:01:00Z", "fecha_fin": "2025-06-19T17:01:00Z"},
        "debe ser posterior a la fecha de inicio"
    ),
    (
        {"fecha_inicio": "2025-06-20T17:01:00Z", "fecha_fin": "2026-06-21T17:01:00Z"},
        "no puede durar mas de un año"
    ),
])
def test_modificar_anuncio_errores_generales(get_authenticated_client, get_anuncio, get_categoria, override_data, expected_error):
    client = get_authenticated_client
    anuncio = get_anuncio
    categoria = get_categoria

    nuevos_datos = {
        "titulo": "Título actualizado",
        "descripcion": "Descripción actualizada",
        "precio_inicial": "20000.00",
        "fecha_inicio": "2025-06-16T12:00:00Z",
        "fecha_fin": "2025-06-21T12:00:00Z",
        "categorias": [categoria.id],
    }

    nuevos_datos.update(override_data)

    response = client.put(f"/api/v3/anuncio/{anuncio.id}/", data=nuevos_datos, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert expected_error.lower() in str(response.data["non_field_errors"][0]).lower()

@pytest.mark.django_db
def test_put_anuncio_usuario_no_autorizado(get_intruso, get_anuncio, get_categoria):
    client, user_intruso = get_intruso
    anuncio = get_anuncio
    categoria = get_categoria

    nuevos_datos = {
        "titulo": "Título actualizado",
        "descripcion": "Descripción actualizada",
        "precio_inicial": "20000.00",
        "fecha_inicio": "2025-06-16T12:00:00Z",
        "fecha_fin": "2025-06-21T12:00:00Z",
        "categorias": [categoria.id],
    }

    response = client.put(f"/api/v3/anuncio/{anuncio.id}/", data=nuevos_datos, format="json")

    assert response.status_code == 403
    assert "No cuenta con el permiso para modificar este anuncio." in str(response.data["detail"])
    assert anuncio.publicado_por != user_intruso

