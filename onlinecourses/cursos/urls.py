from django.urls import include, path
from . import views

app_name = 'cursos'
urlpatterns = [
# /cursos/
     path("", views.index, name='index'),
# /cursos/profile
     path("profile", views.profile, name='profile'),
#pagina login
     path('login', views.loginview, name='login'),
#efetuar logout
     path('logout', views.logoutview, name='logout'),
# /cursos/registar
     path("registar", views.registar, name='registar'),
# /cursos/meuscursos
     path("meuscursos", views.meuscursos, name='meuscursos'),
# ex: /cursos/1
     path('<int:curso_id>', views.detalhe,name='detalhe'),
# ex: /cursos/1/pagamento
     path('<int:curso_id>/pagamento', views.pagamento,name='pagamento'),
# ex: /cursos/search
     path('search', views.search, name='search'),
# ex: /cursos/1/compra
     path('<int:curso_id>/compra', views.compra,name='compra'),
# ex: /cursos/becometeacher
     path('becometeacher', views.becometeacher, name='becometeacher'),
# ex: /cursos/apply
     path('apply', views.apply, name='apply'),
# ex: /cursos/applications
     path('applications', views.applications, name='applications'),
# ex: /cursos/send_email/1
     path('send_email/<int:application_id>/', views.send_email, name='send_email'),
# ex: /cursos/delapplication/1
     path('delapplication/<int:application_id>/', views.delapplication, name='delapplication'),
# ex: /cursos/manageprofessors
     path('manageprofessors', views.manageprofessors, name='manageprofessors'),
# ex: /cursos/manageusers
     path('createprof', views.createprof, name='createprof'),
# ex: /cursos/manageusers
     path('deleteprof', views.deleteprof, name='deleteprof'),
# ex: /cursos/criarcurso
     path('criarcurso', views.criarcurso, name='criarcurso'),
# ex: /cursos/submitcurso
     path('submitcurso', views.submitcurso, name='submitcurso'),
# ex: /cursos/deletecurso/1
     path('deletecurso/<int:curso_id>/', views.deletecurso, name='deletecurso'),
]