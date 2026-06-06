from django.core.exceptions import PermissionDenied
from functools import wraps

def enseignant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.est_enseignant:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def eleve_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.est_eleve:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def classe_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        from classes.models import Classe
        try:
            classe = Classe.objects.get(pk=pk)
            if classe.enseignant != request.user:
                raise PermissionDenied
        except Classe.DoesNotExist:
            raise PermissionDenied
        return view_func(request, pk, *args, **kwargs)
    return wrapper