import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


def create_user(username, documento_identidad, first_name='Micaela', last_name='Salgado', password='unpassword', email=None, *, is_active=True,  is_superuser=False, is_staff=False):
    email = '{}@root.com'.format(username) if email is None else email

    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.documento_identidad = documento_identidad
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.is_staff = is_staff

        user.set_password(password)  # Se Hashea la contraseña al guardarla en la BD
        user.save()

    return user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_user_generico():
    test_user = create_user(username='test_user', documento_identidad='44635875', first_name='Test', last_name='User', email='test@user.com',  is_superuser=True, is_staff=True)
    return test_user


@pytest.fixture
def get_authenticated_client(get_user_generico, api_client):
    token, _ = Token.objects.get_or_create(user=get_user_generico)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client

@pytest.fixture
def get_intruso(api_client):
    intruso = create_user(username="intruso", documento_identidad="99999999",  first_name='intruso', last_name='intruso', email="intruso@root.com", is_superuser=True, is_staff=True)
    token, _ = Token.objects.get_or_create(user=intruso)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client, intruso
