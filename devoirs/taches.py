from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Devoir
from notifications.models import Notification

@shared_task
def envoyer_notifications_deadline():
    """Tâche planifiée: vérifier chaque heure les deadlines à venir."""
    maintenant = timezone.now()
    j2 = maintenant + timedelta(days=2)
    j1 = maintenant + timedelta(days=1)

    # Notifications 2 jours avant
    devoirs_j2 = Devoir.objects.filter(
        deadline__date=j2.date(),
        notif_j2_envoyee=False,
        is_active=True
    )
    for devoir in devoirs_j2:
        eleves = devoir.classe.inscriptions.filter(is_active=True).select_related('eleve')
        for inscription in eleves:
            Notification.objects.create(
                destinataire=inscription.eleve,
                message=f'⏰ Le devoir "{devoir.titre}" est à rendre dans 2 jours.',
                type='deadline',
                lien=f'/devoirs/{devoir.id}/'
            )
        devoir.notif_j2_envoyee = True
        devoir.save(update_fields=['notif_j2_envoyee'])

    # Notifications 1 jour avant
    devoirs_j1 = Devoir.objects.filter(
        deadline__date=j1.date(),
        notif_j1_envoyee=False,
        is_active=True
    )
    for devoir in devoirs_j1:
        eleves = devoir.classe.inscriptions.filter(is_active=True).select_related('eleve')
        for inscription in eleves:
            Notification.objects.create(
                destinataire=inscription.eleve,
                message=f'🚨 Dernier jour ! Le devoir "{devoir.titre}" est à rendre aujourd\'hui.',
                type='urgence',
                lien=f'/devoirs/{devoir.id}/'
            )
        devoir.notif_j1_envoyee = True
        devoir.save(update_fields=['notif_j1_envoyee'])