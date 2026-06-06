from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Devoir, Soumission
from .forms import DevoirForm, SoumissionForm
from classes.models import Classe, Inscription
from classes.permissions import enseignant_required, eleve_required
import os
from django.http import FileResponse, Http404
from django.core.exceptions import PermissionDenied
from classes.models import Classe, Inscription

@login_required
@enseignant_required
def creer_devoir(request, classe_pk):
    classe = get_object_or_404(Classe, pk=classe_pk, enseignant=request.user)
    if request.method == 'POST':
        form = DevoirForm(request.POST, request.FILES)
        if form.is_valid():
            devoir = form.save(commit=False)
            devoir.classe = classe
            devoir.save()
            messages.success(request, f'Devoir "{devoir.titre}" créé avec succès.')
            return redirect('detail_classe', pk=classe_pk)
    else:
        form = DevoirForm()
    return render(request, 'enseignant/creer_devoir.html', {'form': form, 'classe': classe})

@login_required
def detail_devoir(request, pk):
    devoir = get_object_or_404(Devoir, pk=pk, is_active=True)
    # Vérifier que l'utilisateur a accès
    if request.user.est_enseignant:
        if devoir.classe.enseignant != request.user:
            messages.error(request, 'Accès refusé.')
            return redirect('dashboard')
        soumissions = devoir.soumissions.select_related('eleve').all()
        return render(request, 'enseignant/detail_devoir.html', {
            'devoir': devoir,
            'soumissions': soumissions,
            'nb_inscrits': devoir.classe.nombre_eleves,
        })
    else:
        inscription = Inscription.objects.filter(
            eleve=request.user, classe=devoir.classe, is_active=True
        ).exists()
        if not inscription:
            messages.error(request, 'Tu n\'es pas inscrit à cette classe.')
            return redirect('dashboard')
        soumission = Soumission.objects.filter(eleve=request.user, devoir=devoir).first()
        return render(request, 'eleve/detail_devoir.html', {
            'devoir': devoir,
            'soumission': soumission,
            'expire': devoir.est_expire,
        })

@login_required
@eleve_required
def soumettre_devoir(request, pk):
    devoir = get_object_or_404(Devoir, pk=pk, is_active=True)
    if devoir.est_expire:
        messages.error(request, 'La deadline est dépassée, tu ne peux plus soumettre.')
        return redirect('detail_devoir', pk=pk)
    deja_soumis = Soumission.objects.filter(eleve=request.user, devoir=devoir).exists()
    if deja_soumis:
        messages.warning(request, 'Tu as déjà soumis ce devoir.')
        return redirect('detail_devoir', pk=pk)
    if request.method == 'POST':
        form = SoumissionForm(request.POST, request.FILES)
        if form.is_valid():
            soumission = form.save(commit=False)
            soumission.eleve = request.user
            soumission.devoir = devoir
            soumission.save()
            messages.success(request, 'Devoir soumis avec succès !')
            return redirect('detail_devoir', pk=pk)
    else:
        form = SoumissionForm()
    return render(request, 'eleve/soumettre_devoir.html', {'form': form, 'devoir': devoir})
    
@login_required
def servir_soumission(request, pk):
    """
    Sert le fichier d'une soumission uniquement à :
    - L'élève qui a soumis
    - L'enseignant de la classe concernée
    """
    soumission = get_object_or_404(Soumission, pk=pk)

    est_eleve_proprio = request.user == soumission.eleve
    est_enseignant_classe = request.user == soumission.devoir.classe.enseignant

    if not (est_eleve_proprio or est_enseignant_classe):
        raise PermissionDenied

    fichier_path = soumission.fichier.path
    if not os.path.exists(fichier_path):
        raise Http404("Fichier introuvable.")

    return FileResponse(
        open(fichier_path, 'rb'),
        as_attachment=False,
        filename=os.path.basename(fichier_path)
    )


@login_required
def servir_devoir(request, pk):
    """
    Sert le fichier joint d'un devoir uniquement aux :
    - Élèves inscrits à la classe
    - L'enseignant propriétaire
    """
    devoir = get_object_or_404(Devoir, pk=pk)

    est_enseignant = request.user == devoir.classe.enseignant
    est_eleve_inscrit = Inscription.objects.filter(
        eleve=request.user,
        classe=devoir.classe,
        is_active=True
    ).exists()

    if not (est_enseignant or est_eleve_inscrit):
        raise PermissionDenied

    if not devoir.fichier:
        raise Http404("Ce devoir n'a pas de fichier joint.")

    fichier_path = devoir.fichier.path
    if not os.path.exists(fichier_path):
        raise Http404("Fichier introuvable.")

    return FileResponse(
        open(fichier_path, 'rb'),
        as_attachment=False,
        filename=os.path.basename(fichier_path)
    )