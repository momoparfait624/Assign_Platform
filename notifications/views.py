from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def liste_notifications(request):
    notifications = Notification.objects.filter(destinataire=request.user)
    return render(request, 'notifications/liste.html', {'notifications': notifications})

@login_required
def marquer_lue(request, pk):
    notif = get_object_or_404(Notification, pk=pk, destinataire=request.user)
    notif.is_lue = True
    notif.save()
    if notif.lien:
        return redirect(notif.lien)
    return redirect('liste_notifications')

@login_required
def marquer_toutes_lues(request):
    Notification.objects.filter(destinataire=request.user, is_lue=False).update(is_lue=True)
    return redirect('liste_notifications')

@login_required
def nb_non_lues(request):
    count = Notification.objects.filter(destinataire=request.user, is_lue=False).count()
    return JsonResponse({'count': count})