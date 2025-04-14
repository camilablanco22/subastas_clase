from rest_framework import routers
from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet

#Initializarel router de DRF solo unavez
router = routers.DefaultRouter()
# Registrar un ViewSet
router.register(prefix='categoria', viewset=CategoriaViewSet)
router.register(prefix='anuncio', viewset=AnuncioViewSet)