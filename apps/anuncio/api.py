from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.anuncio.models import Categoria, Anuncio
from apps.anuncio.serializers import CategoriaSerializer, AnuncioSerializer, AnuncioReadSerializer
from apps.usuario.models import Usuario


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
        user = Usuario.objects.first()
        serializer = AnuncioSerializer(anuncio, data=request.data)
        if serializer.is_valid():
            serializer.save(publicado_por=user)
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




