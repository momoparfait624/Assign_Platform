from django.urls import path
from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    path('dashboard/eleve/', views.dashboard_eleve, name='dashboard_eleve'),
    path('profil/', views.profil, name='profil'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    path('dashboard/eleve/', views.dashboard_eleve, name='dashboard_eleve'),
    path('profil/', views.profil, name='profil'),
]
path('verifier-session/', views.verifier_session, name='verifier_session'),