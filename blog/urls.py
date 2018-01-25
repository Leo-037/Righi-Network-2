from django.urls import path, include

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
	path('', post_list, name = 'list'),
	# url(r'^word/', redirect_home),
	# url(r'^tag/', redirect_home),
	path('blog/', include([
		path('', redirect_home),
		path('create/', post_create, name = 'create'),
		path('<slug:slug>/', post_detail, name = 'detail'),
		path('<slug:slug>/edit/', post_update, name = 'update'),
		path('<slug:slug>/delete/', post_delete, name = 'delete'),
		path('<slug:slug>/add_tag/<str:tag>/', add_tag, name = 'add-tag'),
		path('<slug:slug>/remove_tag/<str:tag>/', remove_tag, name = 'remove-tag'),
    ])),
	# url(r'^(?P<search_by>[\w-]+)/(?P<query>[\w+-]+)/', post_list, name='list'),
]
