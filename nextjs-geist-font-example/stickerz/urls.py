from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('stickers.urls')),
    path('users/', include('users.urls')),
    path('categories/', include('categories.urls')),
    path('cities/', include('cities.urls')),
    path('notifications/', include('notifications.urls')),
    path('search/', include('search.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('social/', include('social.urls', namespace='social_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
