from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, ProfilForm

def inscription(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # ── Spécifie le backend explicitement ──
            login(request, user, backend='accounts.backends.EmailBackend')
            messages.success(request, f'Bienvenue {user.prenom} ! Votre compte a été créé.')
            return redirect('dashboard')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/register.html', {'form': form})

def connexion(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='accounts.backends.EmailBackend')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = ConnexionForm()
    return render(request, 'accounts/login.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def dashboard(request):
    if request.user.est_enseignant:
        return redirect('dashboard_enseignant')
    return redirect('dashboard_eleve')

@login_required
def dashboard_enseignant(request):
    from classes.models import Classe
    from devoirs.models import Devoir, Soumission

    classes = Classe.objects.filter(
        enseignant=request.user,
        is_active=True
    )

    # Calcul correct des statistiques
    total_eleves = sum(c.nombre_eleves for c in classes)
    total_devoirs = sum(c.devoirs.filter(is_active=True).count() for c in classes)
    total_soumissions = sum(
        Soumission.objects.filter(
            devoir__classe=c
        ).count()
        for c in classes
    )

    return render(request, 'enseignant/dashboard.html', {
        'classes': classes,
        'total_eleves': total_eleves,
        'total_devoirs': total_devoirs,
        'total_soumissions': total_soumissions,
    })

@login_required
def dashboard_eleve(request):
    from classes.models import Inscription
    from devoirs.models import Devoir
    from django.utils import timezone
    inscriptions = Inscription.objects.filter(eleve=request.user, is_active=True)
    classes_ids = inscriptions.values_list('classe_id', flat=True)
    devoirs = Devoir.objects.filter(
        classe_id__in=classes_ids,
        is_active=True
    ).order_by('deadline')
    return render(request, 'eleve/dashboard.html', {'devoirs': devoirs, 'inscriptions': inscriptions})

@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
    else:
        form = ProfilForm(instance=request.user)
    return render(request, 'accounts/profil.html', {'form': form})


def csrf_failure(request, reason=""):
    """Page personnalisée pour les erreurs CSRF."""
    return render(request, 'accounts/csrf_failure.html', status=403)

from django.http import JsonResponse

@login_required
def verifier_session(request):
    """
    Endpoint appelé par le JavaScript toutes les 30 secondes
    pour vérifier si la session est encore active.
    """
    return JsonResponse({'active': True})  

    from django.http import JsonResponse

@login_required
def verifier_session(request):
    return JsonResponse({'active': True})  