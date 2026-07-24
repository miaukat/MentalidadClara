from django import forms
from .models import PerfilUsuario

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['foto', 'telefono', 'biografia']
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: +57 3152584556'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Escribe una breve descripción profesional...'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Recogemos el usuario para saber su rol
        user = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        
        # Si es un PACIENTE, le quitamos el campo de biografía del formulario
        if user and hasattr(user, 'perfil') and user.perfil.rol == 'PACIENTE':
            if 'biografia' in self.fields:
                del self.fields['biografia']