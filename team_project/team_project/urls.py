from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from homepage.views import register_user

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/register/', register_user),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('', include('events.urls')),
    path('events/', include('events.urls')),
    path('api/admin/', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


