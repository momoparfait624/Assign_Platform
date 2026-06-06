import uuid
from django.db import models
from django.conf import settings

class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_acces = models.CharField(max_length=12, unique=True, editable=False)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    enseignant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classes_enseignees',
        limit_choices_to={'role': 'enseignant'}
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code_acces:
            self.code_acces = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    @property
    def nombre_eleves(self):
        return self.inscriptions.filter(is_active=True).count()

    def __str__(self):
        return f"{self.nom} — {self.enseignant}"

class Inscription(models.Model):
    eleve = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        limit_choices_to={'role': 'eleve'}
    )
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('eleve', 'classe')

    def __str__(self):
        return f"{self.eleve} dans {self.classe}"