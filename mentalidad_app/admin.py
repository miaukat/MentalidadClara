from django.contrib import admin
from .models import PerfilUsuario, RegistroEmocional, HorarioDisponible, Cita, Actividad

admin.site.register(PerfilUsuario)
admin.site.register(RegistroEmocional)
admin.site.register(HorarioDisponible)
admin.site.register(Cita)
admin.site.register(Actividad)

