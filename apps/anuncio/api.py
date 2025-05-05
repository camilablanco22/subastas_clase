from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from datetime import datetime, timezone
from rest_framework.exceptions import PermissionDenied

from apps.anuncio.filters import CategoriaFilter, AnuncioFilter
from apps.anuncio.models import Categoria, Anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer, AnuncioReadSerializer

#-----------------------View sets--------------------------------------#
class CategoriaV3(viewsets.ModelViewSet):
    #-------intento de solucion de permisos
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    #-------
    queryset= Categoria.objects.all()
    serializer_class= CategoriaSerializer
    #filterset_fields = ['nombre','activa']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    #filtros de orden
    ordering_fields = ['nombre','activa']

    #para generar un filtro fijo
    """def get_queryset(self):
        return Categoria.objects.filter(nombre__istartswith='m')"""


    """def get_queryset(self):
        queryset = Categoria.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        if nombre is not None:
            queryset = queryset.filter(nombre=nombre)
        return queryset"""



class AnuncioV3(viewsets.ModelViewSet):
    # -------intento de solucion de permisos
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    # -------
    queryset= Anuncio.objects.all()
    filterset_class = AnuncioFilter
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AnuncioReadSerializer
        return AnuncioSerializer

    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user) #usuario autenticado

    def perform_update(self, serializer):
        anuncio = self.get_object()
        if anuncio.publicado_por != self.request.user:
            raise PermissionDenied("No cuenta con el permiso para modificar este anuncio.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.publicado_por != self.request.user:
            raise PermissionDenied("No cuenta con el permiso para eliminar este anuncio.")
        instance.delete()

    @action(detail=True, methods=['get'])
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()
        ahora = datetime.now(timezone.utc)
        fecha_fin = anuncio.fecha_fin

        if fecha_fin < ahora:
            return Response({"mensaje": "El anuncio ya finalizó."})

        diferencia = fecha_fin - ahora
        dias = diferencia.days
        horas, resto = divmod(diferencia.seconds, 3600)
        minutos, _ = divmod(resto, 60)

        return Response({
            "días": dias,
            "horas": horas,
            "minutos": minutos,
            "fecha_fin": anuncio.fecha_fin
        })


#-----------------------Vistas Genéricas--------------------------------------#
class CategoriaListaV2(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleV2(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioListaV2(ListCreateAPIView):
    queryset = Anuncio.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnuncioReadSerializer
        return AnuncioSerializer

    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)


class AnuncioDetalleV2(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnuncioReadSerializer
        return AnuncioSerializer







#-----------------------Vistas APIView--------------------------------------#
class AnuncioListaV1(APIView):
    def get(self, request, format = None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioReadSerializer(anuncios, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = AnuncioSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(publicado_por=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AnuncioDetalleV1(APIView):
    def get(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioReadSerializer(anuncio)
        return Response(serializer.data)

    def put(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CategoriaListaV1(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class CategoriaDetalleV1(APIView):
    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




