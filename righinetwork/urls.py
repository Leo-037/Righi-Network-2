from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import login_view

urlpatterns = [
    # url(r'^account/logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^hijack/', include('hijack.urls')),
    url(r'^login/', login_view),
    url(r'^', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
