from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuario.forms import UsuarioCreationForm
from apps.usuario.models import Usuario


# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    model = Usuario

    list_display = ('username', 'email', 'documento_identidad', 'is_staff')
    search_fields = ('username', 'documento_identidad', 'email')

    # Campos que se muestran al crear un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'documento_identidad', 'domicilio', 'email', 'password1', 'password2'),
        }),
    )

    # Campos que se muestran al editar un usuario existente
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('documento_identidad', 'domicilio', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )