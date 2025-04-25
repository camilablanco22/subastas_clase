from rest_framework import routers
from apps.anuncio.api import CategoriaV3, AnuncioV3

#Initializarel router de DRF solo unavez
router_v3 = routers.DefaultRouter()
# Registrar un ViewSet
router_v3.register(prefix='categoria', viewset=CategoriaV3)
router_v3.register(prefix='anuncio', viewset=AnuncioV3)