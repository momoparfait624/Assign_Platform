from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('classes/', include('classes.urls')),
    path('devoirs/', include('devoirs.urls')),
    path('notifications/', include('notifications.urls')),
    path('', include('accounts.urls')),
]

# En développement — sert uniquement les avatars librement
# Les fichiers devoirs/soumissions sont protégés par les vues dédiées
if settings.DEBUG:
    urlpatterns += static('/media/avatars/', document_root=settings.MEDIA_ROOT / 'avatars')