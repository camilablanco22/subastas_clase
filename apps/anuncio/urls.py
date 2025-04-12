from django.urls import path

from apps.anuncio.api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView

app_name = 'anuncio'

urlpatterns = [
    path('categoria/', CategoriaListaAPIView.as_view()),
    path('categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
    path('anuncio/', AnuncioListaAPIView.as_view()),
    path('anuncio/<int:pk>/', AnuncioDetalleAPIView.as_view())
]