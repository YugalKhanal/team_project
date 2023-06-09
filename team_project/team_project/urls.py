from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from homepage.views import register_user
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
# import csrf exempt
from django.views.decorators.csrf import csrf_exempt
from homepage import views

urlpatterns = [
    # path('admin/', admin.site.urls, name='admin'),
    path('api/v1/register/', register_user),
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('', include('events.urls')),
    path('', include('authentication.urls')),
    path('events/', include('events.urls')),
    path('api/v1/forums/', include('forum.urls')),
    path('', include('forum.urls')),
    path('api/v1/', include('forum.urls')),
    path('', include('help_section.urls')),
    path('help/', include('help_section.urls')),
    path('api/v1/', include('homepage.urls')),
    path('api/admin/', csrf_exempt (admin.site.urls), name='admin'),
    path('api/v1/admin/', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


