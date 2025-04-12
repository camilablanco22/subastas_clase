from rest_framework import serializers
from .models import Categoria, Anuncio


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Categoria
        fields= [
            'id',
            'nombre',
            'activa',
        ]

class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)
    publicado_por = serializers.StringRelatedField(many = False)
    oferta_ganadora = serializers.StringRelatedField(many = False)
    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'fecha_inicio',
            'fecha_fin',
            'fecha_publicacion',
            'categorias',
            'activo',
            'publicado_por',
            'oferta_ganadora'
        ]
        read_only_fields =[
            'publicado_por',
            'oferta_ganadora',
            'fecha_publicacion',
            ]

class AnuncioReadSerializer(serializers.ModelSerializer):
    categorias = serializers.StringRelatedField(many=True)
    publicado_por = serializers.StringRelatedField(many = False)
    oferta_ganadora = serializers.StringRelatedField(many = False)
    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'fecha_inicio',
            'fecha_fin',
            'fecha_publicacion',
            'categorias',
            'activo',
            'publicado_por',
            'oferta_ganadora'
        ]
        read_only_fields =[
            'publicado_por',
            'oferta_ganadora',
            'fecha_publicacion',
            ]