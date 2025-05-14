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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

from subastas_clase.router import router_v3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v3/', include(router_v3.urls)),
    path('api/', include('apps.anuncio.urls', namespace='anuncio')),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')), #-------intento de solucion de permisos

    # Ruta para generarel esquema OpenAPI
     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
     # DocumentaciónSwagger interactiva
     path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
     # DocumentaciónRedoc (estáticay ordenada)
     path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

