from django import forms
from .models import Devoir, Soumission

class DevoirForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = ['titre', 'description', 'fichier', 'deadline']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre du devoir'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Consignes du devoir'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deadline'].input_formats = ['%Y-%m-%dT%H:%M']

class SoumissionForm(forms.ModelForm):
    class Meta:
        model = Soumission
        fields = ['fichier', 'commentaire']
        widgets = {
            'commentaire': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Commentaire (optionnel)'}),
        }