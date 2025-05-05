from django.contrib.auth.forms import UserCreationForm

from apps.usuario.models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'documento_identidad', 'domicilio', 'email')