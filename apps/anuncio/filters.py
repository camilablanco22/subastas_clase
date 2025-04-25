from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria, Anuncio

class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains') #sobreescribo filtro del campo nombre para que use otro lookup
    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']


class AnuncioFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains') #sobreescribo filtro del campo nombre para que use otro lookup
    precio_min = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    precio_max = filters.NumberFilter(field_name='precio_inicial', lookup_expr='lte')
    #categorias = filters.CharFilter(field_name='categorias__nombre', lookup_expr='icontains')
    categorias = filters.ModelMultipleChoiceFilter(
        field_name='categorias__nombre',
        to_field_name='nombre',
        queryset=Categoria.objects.all(),
        conjoined=True  # FALSE = 'or' TRUE = 'and'
    )

    class Meta:
        model = Anuncio
        fields = [
            'titulo',
            'precio_min',
            'precio_max',
            'activo',
            'categorias',
        ]