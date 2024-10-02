from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
# Create your views here.
def cadastro(request):
   if request.method == "GET":
    return render(request, 'cadastro.html')
   elif request.method == "POST":

      username = request.POST.get('username')
      email = request.POST.get('email')
      senha = request.POST.get('senha')
      confirma_senha = request.POST.get('confirmar_senha')

      if senha != confirma_senha:
         messages.add_message(request, constants.ERROR, 'A senha nao esta igual ao confirma senha')

         return redirect('/usuarios/cadastro')
      
      if len(senha) < 6:
         messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')

         return redirect('/usuarios/cadastro')
      
      users = User.objects.filter(username=username)
   
      if users.exists():
         messages.add_message(request, constants.ERROR, 'ja existe um usuario')

         return HttpResponse('/cadastro/usuarios')
   
   
      
      users = User.objects.create_user(

         username=username,
         email=email,
         password=senha,

      )
      
      return redirect ('login')
   
def login_views(request):
   if request.method == "GET":
      print(request.user)
      return render(request, 'login.html')
   
   elif request.method == "POST":
      Username = request.POST.get('Username')
      senha = request.POST.get('senha')
      

   User = auth.authenticate(request, username=Username, password=senha)
   if User:
      auth.login(request,User)
      return redirect('/paciente/home')
   
   messages.add_message(request, constants.ERROR, 'usuario ou senha invalidos')
   return redirect('/usuarios/login')

def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')