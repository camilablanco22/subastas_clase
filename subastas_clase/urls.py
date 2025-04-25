"""
URL configuration for subastas_clase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from subastas_clase.router import router_v3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v3/', include(router_v3.urls)), #no utilizamos path('view-set/', include('subastas_api.router')),
                                            #porque no funciona
    path('api/', include('apps.anuncio.urls', namespace='anuncio')),

]

"""router_v1 = DefaultRouter()
router_v1.register(r'anuncios', AnuncioListaAPIViewV1)
router_v1.register(r'anuncios', AnuncioDetalleAPIViewV1)

router_v2 = DefaultRouter()
router_v2.register(r'usuarios', UsuarioViewSetV2)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.anuncio.urls', namespace='anuncio')),
    path('api/v2/', include(router_v2.urls)),
]
"""