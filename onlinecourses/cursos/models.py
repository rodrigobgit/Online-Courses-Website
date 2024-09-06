from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='profile_image', default='defaultuser.png', null=True, blank=True)


class Professor(models.Model):
    Utilizador = models.OneToOneField(Utilizador, on_delete=models.CASCADE)
    area = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def is_same_area(self, nome_area):
        return self.area == nome_area

class Curso(models.Model):
    descricao = models.CharField(max_length=100)
    area = area = models.CharField(max_length=30)
    vendas = models.IntegerField(default=0)
    data_publicamento = models.DateTimeField(default=timezone.now)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='curso_image/', default='defaultcourse.png')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

class Cliente(models.Model):
    Utilizador = models.OneToOneField(Utilizador, on_delete=models.CASCADE)
    ocupacao = models.CharField(max_length=30)

#Necessário porque é uma relação muitos para muitos entre cliente e curso
class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(default=timezone.now)
    num_cartao = models.IntegerField(max_length=16)
    dat_expir = models.DateTimeField(default=timezone.now())
    cvv = models.IntegerField(max_length=3)

class Application(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    area_of_expertise = models.CharField(max_length=100)
    certification = models.FileField(upload_to='certifications/')
    approved = models.BooleanField(default=False)


class Content(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='contents/')

