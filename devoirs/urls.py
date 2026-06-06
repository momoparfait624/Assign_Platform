from django.urls import path
from . import views

urlpatterns = [
    path('classe/<uuid:classe_pk>/creer/', views.creer_devoir, name='creer_devoir'),
    path('<uuid:pk>/', views.detail_devoir, name='detail_devoir'),
    path('<uuid:pk>/soumettre/', views.soumettre_devoir, name='soumettre_devoir'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('classe/<uuid:classe_pk>/creer/', views.creer_devoir, name='creer_devoir'),
    path('<uuid:pk>/', views.detail_devoir, name='detail_devoir'),
    path('<uuid:pk>/soumettre/', views.soumettre_devoir, name='soumettre_devoir'),
    # ── Protection fichiers media ──────────────────────────────
    path('fichier/soumission/<uuid:pk>/', views.servir_soumission, name='servir_soumission'),
    path('fichier/devoir/<uuid:pk>/', views.servir_devoir, name='servir_devoir'),
]