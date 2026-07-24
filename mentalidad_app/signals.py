from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@receiver(post_save, sender=User)
def gestionar_usuario_nuevo(sender, instance, created, **kwargs):
    """
    Señal única que asegura el perfil y envía el correo de bienvenida 
    utilizando la plantilla correcta según el rol del usuario.
    """
    if created and instance.email:
        # 1. Asegurar que el PerfilUsuario exista por seguridad
        from .models import PerfilUsuario
        perfil, _ = PerfilUsuario.objects.get_or_create(usuario=instance)

        # 2. Seleccionar la plantilla HTML y el asunto según el rol
        if perfil.rol == 'TERAPEUTA':
            plantilla_html = 'emails/bienvenida_terapeuta.html'
            asunto = "🩺 ¡Bienvenido/a al equipo profesional de Mentalidad Clara!"
        elif perfil.rol == 'PACIENTE':
            plantilla_html = 'emails/bienvenida_paciente.html'
            asunto = "🌱 ¡Bienvenido/a a Mentalidad Clara!"
        else:
            # Plantilla por defecto para administradores u otros roles
            plantilla_html = 'emails/bienvenida.html'
            asunto = "🌱 ¡Bienvenido/a a Mentalidad Clara!"

        remitente = settings.DEFAULT_FROM_EMAIL
        destinatarios = [instance.email]

        # 3. Renderizar el correo pasando los datos necesarios al contexto
        contexto = {
            'usuario': instance,
            'perfil': perfil,
            'nombre': instance.first_name,
            'apellido': instance.last_name,
            'username': instance.username,
        }
        
        try:
            html_content = render_to_string(plantilla_html, contexto)
            text_content = strip_tags(html_content)

            correo = EmailMultiAlternatives(asunto, text_content, remitente, destinatarios)
            correo.attach_alternative(html_content, "text/html")
            correo.send()
            
            print(f"✅ Correo enviado con la plantilla '{plantilla_html}' a {instance.email}")
        except Exception as e:
            print(f"❌ Error al enviar correo de bienvenida: {e}")