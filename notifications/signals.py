from django.db.models.signals import post_save
from django.dispatch import receiver
from devoirs.models import Devoir, Soumission
from .models import Notification


@receiver(post_save, sender=Devoir)
def notifier_nouveau_devoir(sender, instance, created, **kwargs):
    """
    Dès qu'un devoir est créé, notifier tous les élèves de la classe.
    """
    if created:
        inscriptions = instance.classe.inscriptions.filter(
            is_active=True
        ).select_related('eleve')

        notifications = [
            Notification(
                destinataire=inscription.eleve,
                message=f'📚 Nouveau devoir : "{instance.titre}" dans la classe {instance.classe.nom}. Deadline : {instance.deadline.strftime("%d/%m/%Y à %H:%M")}.',
                type='info',
                lien=f'/devoirs/{instance.pk}/'
            )
            for inscription in inscriptions
        ]
        # Création en masse pour optimiser les requêtes
        Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=Soumission)
def notifier_soumission_recue(sender, instance, created, **kwargs):
    """
    Notifier l'enseignant quand un élève soumet un devoir.
    """
    if created:
        enseignant = instance.devoir.classe.enseignant
        Notification.objects.create(
            destinataire=enseignant,
            message=f'✅ {instance.eleve.prenom} {instance.eleve.nom} a soumis le devoir "{instance.devoir.titre}".',
            type='info',
            lien=f'/devoirs/{instance.devoir.pk}/'
        )