from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Classe, Inscription
from .forms import ClasseForm, RejoindreClasseForm
from .permissions import enseignant_required, eleve_required, classe_owner_required

@login_required
@enseignant_required
def creer_classe(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            classe = form.save(commit=False)
            classe.enseignant = request.user
            classe.save()
            messages.success(request, f'Classe "{classe.nom}" créée ! Code : {classe.code_acces}')
            return redirect('detail_classe', pk=classe.pk)
    else:
        form = ClasseForm()
    return render(request, 'enseignant/creer_classe.html', {'form': form})

@login_required
@enseignant_required
@classe_owner_required
def detail_classe(request, pk):
    classe = get_object_or_404(Classe, pk=pk, is_active=True)
    inscriptions = classe.inscriptions.filter(is_active=True).select_related('eleve')
    devoirs = classe.devoirs.filter(is_active=True).order_by('deadline')
    return render(request, 'enseignant/detail_classe.html', {
        'classe': classe,
        'inscriptions': inscriptions,
        'devoirs': devoirs,
    })

@login_required
@enseignant_required
@classe_owner_required
def supprimer_classe(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        classe.is_active = False
        classe.save()
        messages.success(request, f'Classe "{classe.nom}" supprimée.')
        return redirect('dashboard_enseignant')
    return render(request, 'enseignant/confirmer_suppression.html', {'classe': classe})

@login_required
@eleve_required
def rejoindre_classe(request):
    if request.method == 'POST':
        form = RejoindreClasseForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code_acces'].upper()
            try:
                classe = Classe.objects.get(code_acces=code, is_active=True)
                inscription, creee = Inscription.objects.get_or_create(
                    eleve=request.user, classe=classe
                )
                if creee:
                    messages.success(request, f'Tu as rejoint la classe "{classe.nom}" !')
                else:
                    inscription.is_active = True
                    inscription.save()
                    messages.info(request, f'Tu es déjà inscrit à "{classe.nom}".')
                return redirect('dashboard_eleve')
            except Classe.DoesNotExist:
                messages.error(request, 'Code d\'accès invalide.')
    else:
        form = RejoindreClasseForm()
    return render(request, 'eleve/rejoindre_classe.html', {'form': form})

@login_required
@eleve_required
def quitter_classe(request, pk):
    inscription = get_object_or_404(Inscription, classe_id=pk, eleve=request.user)
    if request.method == 'POST':
        inscription.is_active = False
        inscription.save()
        messages.success(request, 'Tu as quitté la classe.')
        return redirect('dashboard_eleve')
    return render(request, 'eleve/confirmer_quitter.html', {'inscription': inscription})