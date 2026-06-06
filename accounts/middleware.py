import datetime
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    URLS_EXCLUES = [
        '/accounts/',
        '/accounts/inscription/',
        '/accounts/verifier-session/',
        '/admin/',
        '/static/',
        '/media/',
    ]

    def __call__(self, request):
        # Ignore toutes les URLs publiques
        for url in self.URLS_EXCLUES:
            if request.path.startswith(url):
                return self.get_response(request)

        # Ignore si l'utilisateur n'est pas connecté
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Vérifie l'expiration
        derniere_activite = request.session.get('derniere_activite')

        if derniere_activite:
            try:
                derniere_activite = datetime.datetime.fromisoformat(
                    derniere_activite
                )
                duree = (
                    datetime.datetime.now() - derniere_activite
                ).total_seconds()

                if duree > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('/?session_expired=1')

            except (ValueError, TypeError):
                pass

        # Met à jour l'horodatage
        request.session['derniere_activite'] = (
            datetime.datetime.now().isoformat()
        )

        return self.get_response(request)