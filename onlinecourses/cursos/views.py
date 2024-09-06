from django.contrib.auth.decorators import *
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login , logout
from django.template import loader
from .models import Curso, Professor, Utilizador, User, Compra, Cliente, Application, Content
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

#mostra pagina inicial
def index(request):
    return render(request, 'cursos/index.html')

#funcao auxiliar que verifica se user -> admin
def check_superuser(user):
    return user.is_superuser

def check_professor(user):
    return user.is_authenticated and not user.is_superuser and hasattr(user.utilizador, 'professor')


def search(request):
    query = request.GET.get('q')
    cursos = Curso.objects.filter(Q(descricao__icontains=query))
    return render(request, 'cursos/search_results.html', {'cursos': cursos})

@login_required(login_url=reverse_lazy('cursos:login'))
def detalhe(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    conteudos = Content.objects.filter(curso=curso)
    vendas = Compra.objects.filter(curso=curso).count()
    if not check_superuser(request.user) and not check_professor(request.user):

        cliente = request.user.utilizador.cliente
        compra = Compra.objects.filter(cliente=cliente, curso=curso).first()
        if compra is None:
            return redirect('cursos:pagamento', curso_id=curso.id)
    return render(request, 'cursos/detalhe.html', {'curso': curso, 'conteudos': conteudos,'vendas': vendas})

@login_required(login_url=reverse_lazy('cursos:login'))
def compra(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        card_number = request.POST.get('cardNumber')
        card_number_without_space = card_number.replace(" ", "")
        card_number_int = int(card_number_without_space)
        card_name = request.POST.get('cardName')
        expiry_month = request.POST.get('expiryMonth')
        expiry_year = request.POST.get('expiryYear')
        cvv = request.POST.get('cvv')
        cliente = Cliente.objects.get(Utilizador=request.user.utilizador)
        compra = Compra.objects.create(
            cliente=cliente,
            curso=curso,
            data_compra=timezone.now(),
            num_cartao=card_number_int,
            dat_expir=timezone.datetime(int(expiry_year), int(expiry_month), 1).replace(day=28) + timezone.timedelta(
                days=3),
            cvv=cvv,
        )
        compra.save()
        return HttpResponseRedirect(reverse('cursos:detalhe', args=(curso_id,)))

@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def applications(request):
    applications = Application.objects.filter(approved=False)
    return render(request,'cursos/applications.html',{'applications': applications})
@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def send_email(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    application.approved = True
    application.save()
    send_mail(
        'Application',
        'Your application has been accepted! Please get back to us and let us know which username and password combination you would like.',
        'bestecourses.recruitment@gmail.com',
        [application.email],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse('cursos:applications'))
@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def delapplication(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    application.delete()
    return HttpResponseRedirect(reverse('cursos:applications'))

@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def manageprofessors(request):
    return render(request, 'cursos/manageprofessors.html')



def apply(request):
    if request.method == 'POST' and request.FILES['myfile']:

        prim_nome = request.POST.get('primnome')
        ult_nome = request.POST.get('ultnome')
        email = request.POST.get('email')
        numero = request.POST.get('numero')
        area = request.POST.get('area')
        file = request.FILES['myfile']



        application = Application(
            first_name=prim_nome,
            last_name=ult_nome,
            email=email,
            phone_number=numero,
            area_of_expertise=area,
            certification=file,
        )
        application.save()

        # Redirect to success page
        return HttpResponseRedirect(reverse('cursos:index'))

        # Render the application page
    return render(request, 'cursos/becometeacher.html')

def becometeacher(request):
    return render(request, 'cursos/becometeacher.html')

def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('cursos:index'))
        else:
            return render(request, 'cursos/login.html', {
                'error_message': "Wrong username/password", })

    return render(request, 'cursos/login.html')

@login_required(login_url=reverse_lazy('cursos:login'))
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('cursos:login'))

@login_required(login_url=reverse_lazy('cursos:login'))
def pagamento(request, curso_id):
    if not check_superuser(request.user):
        curso = get_object_or_404(Curso, pk=curso_id)
        return render(request, 'cursos/pagamento.html',{'curso': curso})
    else:
        return render(request, 'cursos/login.html', {
            'error_message': "This content is for clients only", })

def registar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'cursos/registar.html', {'error_message': 'A user with that email already exists.'})
        u = User.objects.create_user(username, email, password)
        utilizador = Utilizador(user=u)
        utilizador.save()
        cliente = Cliente(Utilizador=utilizador)
        cliente.save()

        return HttpResponseRedirect(reverse('cursos:login'))
    else:
        return render(request, 'cursos/registar.html')


@login_required(login_url=reverse_lazy('cursos:login'))
def meuscursos(request):
    if not request.user.is_superuser:
        if request.user.utilizador.cliente:
            cliente = request.user.utilizador.cliente
            cursos_comprados = Curso.objects.filter(compra__cliente=cliente)
            cursos = Curso.objects.all()
            return render(request, 'cursos/meuscursos.html', {'cursos': cursos_comprados})
    else:
        return render(request, 'cursos/login.html', {
            'error_message': "This content is for clients only", })

@user_passes_test(check_professor, login_url=reverse_lazy('cursos:login'))
def criarcurso(request):
    return render(request,'cursos/criarcursos.html')

@user_passes_test(check_professor, login_url=reverse_lazy('cursos:login'))
def submitcurso(request):
    if request.method == 'POST':
        # get the data submitted in the form
        descricao = request.POST['descricao']
        preco = request.POST['preco']
        image = request.FILES.get('image')
        titulos_conteudos = request.POST.getlist('titulo_conteudo[]')
        arquivos = request.FILES.getlist('conteudo[]')
        area = request.user.utilizador.professor.area
        if image is None:
            curso = Curso.objects.create(descricao=descricao, professor=request.user.utilizador.professor, preco=preco,area=area)
        else:
            curso = Curso.objects.create(descricao=descricao, professor=request.user.utilizador.professor, preco=preco,
                                         image=image,area=area)

        # create Conteudo instances and add them to the curso
        for i in range(len(titulos_conteudos)):
            titulo_conteudo = titulos_conteudos[i]
            arquivo = arquivos[i]
            conteudo = Content.objects.create(title=titulo_conteudo, file=arquivo,curso=curso)
            conteudo.save()

        # redirect to the newly created curso
        return redirect('cursos:index')

    return render(request, 'cursos/criarcurso.html')

@login_required(login_url=reverse_lazy('cursos:login'))
def profile(request):
    return render(request,'cursos/profile.html')

#admin cria um professor(so o admin pode registar um professor)
@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def createprof(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['emailcreate']
        application = Application.objects.filter(email=email).first()
        if application:
            area = application.area_of_expertise
            u = User.objects.create_user(username, email, password)
            utilizador = Utilizador(user=u)
            utilizador.save()
            prof = Professor.objects.create(Utilizador=utilizador,area=area,email=email)
            prof.save()
            messages.success(request, 'Professor created successfully!')
            return redirect('cursos:manageprofessors')
        else:
            return render(request, 'cursos/manageprofessors.html', {
                    'error_message': "No application for this email!", })
    else:
        return render(request, 'cursos/manageprofessors.html')


@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def deleteprof(request):
    if request.method == 'POST':
        email = request.POST['emaildelete']
        try:
            prof = Professor.objects.get(email=email)
            utilizador = prof.Utilizador
            user = utilizador.user

            prof.delete()
            utilizador.delete()
            user.delete()

            messages.success(request, 'Professor deleted successfully!')
        except Professor.DoesNotExist:
            messages.error(request, 'No professor with this email!')

        return redirect('cursos:manageprofessors')
    else:
        return render(request, 'cursos/manageprofessors.html')

@user_passes_test(check_superuser, login_url=reverse_lazy('cursos:login'))
def deletecurso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    curso.delete()
    return redirect('cursos:index')