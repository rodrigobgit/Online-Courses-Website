from django.contrib.auth.decorators import *
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login , logout
from django.template import loader

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def cursos(request):
    return HttpResponseRedirect(reverse('cursos:index'))

