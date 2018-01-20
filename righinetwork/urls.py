from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import signup_view, change_color_view

urlpatterns = [
	path('accounts/signup/', signup_view),
	path('accounts/', include('allauth.urls')),
	path('admin/', admin.site.urls),
	path('colore/<str:colore>', change_color_view, name = "change_color"),
	path('assemblee/', include('assemblee.urls', namespace = "assemblee")),
	path('gestione/', include('accounts.urls', namespace = 'accounts')),
	path('sondaggi/', include('sondaggi.urls', namespace = "sondaggi")),
	path('merchandising/', include('merchandising.urls', namespace = "merchandising")),
	path('hijack/', include('hijack.urls')),
	path('silk/', include('silk.urls', namespace = 'silk')),
	path('summernote/', include('django_summernote.urls')),
	path('', include('blog.urls', namespace = 'blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
