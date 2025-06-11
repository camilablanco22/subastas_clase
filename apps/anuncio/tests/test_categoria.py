import pytest
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from .fixtures_categoria import get_categorias
from ..models import Categoria


@pytest.mark.django_db
def test_api_lista_categorias(get_authenticated_client, get_categorias):
    cliente = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias
    response = cliente.get(f'/api/v3/categoria/')
    assert response.status_code == 200

    # verificar que se devuelvan las categorias creadas en "get_categorias"
    # tener en cuenta que puede variar el orden de las categorias devueltas en funcion de los parametros iniciales del api


    data = response.data["results"]
    assert data[0]['nombre'] == categoria1.nombre # Computacion
    assert data[1]['nombre'] == categoria2.nombre  # Electronica
    assert data[2]['nombre'] == categoria3.nombre  # Hogar


@pytest.mark.django_db
def test_api_lista_categorias_filtradas(get_authenticated_client, get_categorias):
    cliente = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias

    # se comprueba que la categoria3 está inactiva", por lo cual quedan solo dos categorias activas
    assert categoria1.activa
    assert categoria2.activa
    assert not categoria3.activa

    response = cliente.get(f'/api/v3/categoria/?activa=true')
    assert response.status_code == 200

    # verificar que se devuelvan solo las dos categorias activas

    data = response.data["results"]
    assert len(data) == 2
    assert data[0]['nombre'] == categoria1.nombre # Computacion
    assert data[1]['nombre'] == categoria2.nombre  # Electronica

@pytest.mark.django_db
def test_api_creacion_categoria(get_authenticated_client, get_categorias):
    client = get_authenticated_client

    data = {
        "nombre": "Indumentaria",
    }

    response = client.post(f'/api/v3/categoria/', data=data)
    assert response.status_code == 201
    assert Categoria.objects.filter(nombre='Indumentaria').count() == 1
