import os, uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

def devoir_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    # Sécurisation: seulement pdf, doc, docx, jpg, png
    allowed = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
    if ext not in allowed:
        raise ValueError("Type de fichier non autorisé")
    return f'devoirs/{instance.classe.id}/{uuid.uuid4().hex}.{ext}'

def soumission_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    allowed = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
    if ext not in allowed:
        raise ValueError("Type de fichier non autorisé")
    return f'soumissions/{instance.devoir.id}/{instance.eleve.id}/{uuid.uuid4().hex}.{ext}'

class Devoir(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=300)
    description = models.TextField()
    fichier = models.FileField(upload_to=devoir_upload_path, blank=True, null=True)
    classe = models.ForeignKey('classes.Classe', on_delete=models.CASCADE, related_name='devoirs')
    deadline = models.DateTimeField()  # OBLIGATOIRE
    date_creation = models.DateTimeField(auto_now_add=True)
    notif_j2_envoyee = models.BooleanField(default=False)
    notif_j1_envoyee = models.BooleanField(default=False)
    notif_deadline_envoyee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def est_expire(self):
        return timezone.now() > self.deadline

    @property
    def nombre_soumissions(self):
        return self.soumissions.count()

    def __str__(self):
        return f"{self.titre} — deadline {self.deadline:%d/%m/%Y}"

class Soumission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eleve = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='soumissions',
        limit_choices_to={'role': 'eleve'}
    )
    devoir = models.ForeignKey(Devoir, on_delete=models.CASCADE, related_name='soumissions')
    fichier = models.FileField(upload_to=soumission_upload_path)
    commentaire = models.TextField(blank=True)
    date_soumission = models.DateTimeField(auto_now_add=True)
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('eleve', 'devoir')  # Un seul rendu par élève

    def __str__(self):
        return f"Rendu de {self.eleve} pour {self.devoir.titre}"