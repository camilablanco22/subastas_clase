from decimal import Decimal

import requests
from rest_framework import serializers
from subastas_clase import settings
from .models import Categoria, Anuncio, OfertaAnuncio
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Categoria
        fields= [
            'id',
            'nombre',
            'activa',
        ]

    def validate_nombre(self, value):
        #Verificarque el nombreno contegnala palabra "categoría"
        if "categoria" in value.lower():
            raise serializers.ValidationError("El nombre no puede contener la palabra 'categoria'.")
        return value

    def validate(self, data):
        if 'principal' in data['nombre'] and not data['activa']:
            raise serializers.ValidationError("No se puede desactivar categoria principal.")
        return data



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

    def validate_precio_inicial(self, value):
        #Verificar que el precio inicial de la suabsta sea mayor o igual a cero
        if value <= 0:
            raise serializers.ValidationError("El precio inicial de la subasta debe ser mayor o igual a cero.")
        return value

    def validate_fecha_inicio(self, value):
        #Verificar que el fecha_inicio sea posterior a la fecha actual
        fecha_actual = datetime.now(timezone.utc)

        if value < fecha_actual:
            raise serializers.ValidationError("La fecha de inicio no puede ser anterior a la fecha actual.")

        fecha_actual = datetime.now(timezone.utc)
        fecha_15_dias_despues = fecha_actual + relativedelta(days=15)
        if fecha_15_dias_despues < value:
            raise serializers.ValidationError("La subasta no puede tardar mas de 15 días en iniciar.")
        return value


    def validate(self, data):
        if data['fecha_fin'] < data['fecha_inicio'] :
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        fecha_un_anio_despues = data['fecha_inicio'] + relativedelta(years=1)
        if fecha_un_anio_despues < data['fecha_fin'] :
            raise serializers.ValidationError("El anuncio no puede durar mas de un año.")
        return data


class AnuncioReadSerializer(serializers.ModelSerializer):
    categorias = serializers.StringRelatedField(many=True)
    publicado_por = serializers.StringRelatedField()
    oferta_ganadora = serializers.StringRelatedField()

    precio_usd = serializers.SerializerMethodField()
    precio_eur = serializers.SerializerMethodField()

    class Meta:
        model = Anuncio
        fields = [
            'id', 'titulo', 'descripcion', 'precio_inicial',
            'precio_usd', 'precio_eur',
            'fecha_inicio', 'fecha_fin', 'fecha_publicacion',
            'categorias', 'activo', 'publicado_por', 'oferta_ganadora'
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora', 'fecha_publicacion']

    def get_precio_usd(self, obj):
        return self.convertir_moneda(obj.precio_inicial, 'USD')

    def get_precio_eur(self, obj):
        return self.convertir_moneda(obj.precio_inicial, 'EUR')

    def convertir_moneda(self, monto, moneda_destino):
        url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_API_KEY}/latest/ARS"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("No se pudo obtener la tasa de cambio")

        data = response.json()
        tasa = data['conversion_rates'].get(moneda_destino)

        if tasa is None:
            raise Exception(f"Tasa de cambio no encontrada para {moneda_destino}")

        return round(monto * Decimal(str(tasa)), 2)

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaAnuncio
        fields = ['anuncio', 'fecha_oferta', 'precio_oferta', 'es_ganador', 'usuario']
        read_only_fields = ['usuario', 'anuncio', 'fecha_oferta']