from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class InscriptionForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='Mot de passe'
    )
    confirmer_mdp = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
        label='Confirmer le mot de passe'
    )

    class Meta:
        model = CustomUser
        fields = ['nom', 'prenom', 'email', 'matricule', 'etablissement', 'role', 'avatar']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'matricule': forms.TextInput(attrs={'placeholder': 'Matricule (élèves)'}),
            'etablissement': forms.TextInput(attrs={'placeholder': 'Établissement'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get('mot_de_passe')
        confirm = cleaned_data.get('confirmer_mdp')
        if mdp and confirm and mdp != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['mot_de_passe'])
        if commit:
            user.save()
        return user

class ConnexionForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='Mot de passe'
    )

class ProfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nom', 'prenom', 'matricule', 'etablissement', 'avatar']