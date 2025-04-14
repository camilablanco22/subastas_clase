from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from datetime import datetime, timezone

from apps.anuncio.models import Categoria, Anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer, AnuncioReadSerializer
from apps.usuario.models import Usuario

#-----------------------Vistas Genéricas--------------------------------------#
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnuncioReadSerializer
        return AnuncioSerializer

    def perform_create(self, serializer):
        user = Usuario.objects.first()  # o `self.request.user` si usás autenticación
        serializer.save(publicado_por=user)


class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AnuncioReadSerializer
        return AnuncioSerializer




#-----------------------View sets--------------------------------------#
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset= Categoria.objects.all()
    serializer_class= CategoriaSerializer

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset= Anuncio.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AnuncioReadSerializer
        return AnuncioSerializer

    def perform_create(self, serializer):
        user = Usuario.objects.first()
        serializer.save(publicado_por=user)

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



#-----------------------Vistas APIView--------------------------------------#
class AnuncioListaAPIView(APIView):
    def get(self, request, format = None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioReadSerializer(anuncios, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = AnuncioSerializer(data = request.data)
        user = Usuario.objects.first()
        if serializer.is_valid():
            serializer.save(publicado_por=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AnuncioDetalleAPIView(APIView):
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




class CategoriaListaAPIView(APIView):
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



class CategoriaDetalleAPIView(APIView):
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




