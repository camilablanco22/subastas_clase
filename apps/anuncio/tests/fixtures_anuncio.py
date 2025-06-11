import pytest
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from apps.anuncio.models import Anuncio



@pytest.fixture
def get_anuncio(get_categoria, get_user_generico):
    anuncio, _ = Anuncio.objects.get_or_create(
        titulo = 'Anuncio1',
        defaults={
            "descripcion": "Desc",
            "precio_inicial": "15000.00",
            "fecha_inicio": "2025-06-20T17:01:00Z",
            "fecha_fin": "2025-06-30T17:01:00Z",
            "publicado_por": get_user_generico

        }
    )
    anuncio.categorias.set([get_categoria])
    return anuncio