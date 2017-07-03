from django.conf.urls import url, include

from .views import (
    add_tag,
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    redirect_home,
    remove_tag,
)

app_name = "blog"

urlpatterns = [
    url(r'^$', post_list, name='list'),
    # url(r'^word/$', redirect_home),
    # url(r'^tag/$', redirect_home),
    url(r'^blog/', include([
        url(r'^$', redirect_home),
        url(r'^create/$', post_create, name='create'),
        url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
        url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
        url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
        url(r'^(?P<slug>[\w-]+)/add_tag/(?P<tag>[\w-]+)/$', add_tag, name='add-tag'),
        url(r'^(?P<slug>[\w-]+)/remove_tag/(?P<tag>[\w-]+)/$', remove_tag, name='remove-tag'),
    ])),
    # url(r'^(?P<search_by>[\w-]+)/(?P<query>[\w+-]+)/$', post_list, name='list'),
]
