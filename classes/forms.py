from django import forms
from .models import Classe

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom de la classe'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description (optionnel)', 'rows': 3}),
        }

class RejoindreClasseForm(forms.Form):
    code_acces = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Code d\'accès (ex: A3F9B2C1)'}),
        label="Code d'accès"
    )