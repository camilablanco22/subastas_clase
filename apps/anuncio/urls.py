from django.urls import path

from apps.anuncio.api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView, \
    CategoriaListaGenericView, CategoriaDetalleGenericView, AnuncioListaGenericView, AnuncioDetalleGenericView
from apps.anuncio.models import Anuncio

app_name = 'anuncio'

urlpatterns = [
    path('generic-view/categoria/', CategoriaListaGenericView.as_view()),
    path('generic-view/categoria/<int:pk>/', CategoriaDetalleGenericView.as_view()),
    path('generic-view/anuncio/', AnuncioListaGenericView.as_view()),
    path('generic-view/anuncio/<int:pk>/', AnuncioDetalleGenericView.as_view()),
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncio/', AnuncioListaAPIView.as_view()),
    path('api-view/anuncio/<int:pk>/', AnuncioDetalleAPIView.as_view())
]