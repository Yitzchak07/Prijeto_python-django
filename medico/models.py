from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def is_medico(user):
    return Dadosmedico.objects.filter(user=user).exists()


class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
        return self.especialidade
    
class Dadosmedico(models.Model):
    crm = models.CharField(max_length=35)
    nome = models.CharField(max_length=50)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=120)
    bairro = models.CharField(max_length=120)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to='rgs')
    cedula_indentidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to='foto_perfil')
    descricao = models.TextField()
    valor_consulta = models.FloatField(default=100)
    user = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username
    @property
    def proxima_data(self):
        proxima_data = Datas_abertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendados=False).order_by('data').first()
        return proxima_data
    

class Datas_abertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendados = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)
    