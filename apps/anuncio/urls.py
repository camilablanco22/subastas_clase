from django.urls import path

from apps.anuncio.api import CategoriaListaV1, CategoriaDetalleV1, AnuncioListaV1, AnuncioDetalleV1, \
    CategoriaListaV2, CategoriaDetalleV2, AnuncioListaV2, AnuncioDetalleV2

app_name = 'anuncio'

urlpatterns = [
    path('v2/categoria/', CategoriaListaV2.as_view()),
    path('v2/categoria/<int:pk>/', CategoriaDetalleV2.as_view()),
    path('v2/anuncio/', AnuncioListaV2.as_view()),
    path('v2/anuncio/<int:pk>/', AnuncioDetalleV2.as_view()),
    path('v1/categoria/', CategoriaListaV1.as_view()),
    path('v1/categoria/<int:pk>/', CategoriaDetalleV1.as_view()),
    path('v1/anuncio/', AnuncioListaV1.as_view()),
    path('v1/anuncio/<int:pk>/', AnuncioDetalleV1.as_view())
]