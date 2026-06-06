from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_notifications, name='liste_notifications'),
    path('<uuid:pk>/lire/', views.marquer_lue, name='marquer_lue'),
    path('tout-lire/', views.marquer_toutes_lues, name='marquer_toutes_lues'),
    path('count/', views.nb_non_lues, name='nb_non_lues'),
]