from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import signup_view

urlpatterns = [
    url(r'^accounts/signup/$', signup_view),
    url(r'^accounts/', include('allauth.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^assemblee/', include('assemblee.urls', namespace = "assemblee")),
    url(r'^gestione/', include('accounts.urls', namespace='accounts')),
    url(r'^hijack/', include('hijack.urls')),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
