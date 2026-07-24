from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from mentalidad_app.models import Cita

class Command(BaseCommand):
    help = 'Envía recordatorios por correo a los pacientes con citas programadas para el día siguiente.'

    def handle(self, *args, **kwargs):
        mañana = timezone.now().date() + timezone.timedelta(days=1)
        citas_mañana = Cita.objects.filter(horario__fecha=mañana, estado='CONFIRMADA')
        
        contador = 0
        for cita in citas_mañana:
            if cita.paciente and cita.paciente.email:
                asunto = "Recordatorio: Tienes una cita médica mañana - Mentalidad Clara"
                mensaje = (
                    f"Hola {cita.paciente.get_full_name() or cita.paciente.username},\n\n"
                    f"Te recordamos que tienes una cita programada para el día de mañana:\n\n"
                    f"- Fecha: {mañana.strftime('%d/%m/%Y')}\n"
                    f"- Hora: {cita.horario.hora_inicio.strftime('%I:%M %p')}\n"
                    f"- Terapeuta: Dr(a). {cita.terapeuta.get_full_name() or cita.terapeuta.username}\n\n"
                    f"Si por algún motivo no puedes asistir, por favor ingresa a la plataforma para cancelarla o reprogramarla.\n\n"
                    f"¡Te esperamos!\n"
                    f"Atentamente,\nEquipo de Mentalidad Clara"
                )
                try:
                    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [cita.paciente.email], fail_silently=False)
                    contador += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error enviando correo a {cita.paciente.email}: {e}"))
                    
        self.stdout.write(self.style.SUCCESS(f"Se enviaron {contador} recordatorios correctamente para el día {mañana}."))