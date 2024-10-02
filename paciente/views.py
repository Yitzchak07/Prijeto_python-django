from django.shortcuts import render, redirect
from medico.models import Dadosmedico, Especialidades, Datas_abertas, is_medico
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from .models import Consulta, Documento
# Create your views here.

def home(request):
    if request.method == "GET":
     medicos = Dadosmedico.objects.all()
     medico_filtrar = request.GET.get('medico')
     especialidades_filtrar = request.GET.getlist('especialidades')
    
    if medico_filtrar:
       medicos = medicos.filter(nome__icontains=medico_filtrar)

    if especialidades_filtrar:
       medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

    especialidades = Especialidades.objects.all()
    return render(request, 'home.html',{'medicos': medicos, 'especialidades': especialidades, 'is_medico': is_medico(request.user)})


def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = Dadosmedico.objects.get(id=id_dados_medicos)
        datas_abertas = Datas_abertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendados=False)
        return render(request, 'escolher_horario.html', {'medicos': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = Datas_abertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/paciente/minhas_consultas/')
    
def minhas_consultas(request):
    minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
    return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})

def consulta(request, id_consulta):
   if request.method == 'GET':
      consulta = Consulta.objects.get(id=id_consulta)
      dados_medico = Dadosmedico.objects.get(user=consulta.data_aberta.user)
      documentos = Documento.objects.filter(consulta=consulta)
      return render(request, 'consulta.html', {'consulta': consulta, 'dados_medico': dados_medico, 'documentos': documentos })
      