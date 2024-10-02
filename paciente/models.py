from django.db import models
from django.contrib.auth.models import User
from medico.models import Dadosmedico, Datas_abertas
from datetime import datetime
# Create your models here.

class Consulta(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')

    )
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(Datas_abertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username
    
   
    @property
    def proxima_data(self):
        proxima_data = Datas_abertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendados=False).order_by('data').first()
        return proxima_data
    
class Documento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.titulo
