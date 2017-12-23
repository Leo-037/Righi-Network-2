from django.conf.urls import url

from . import views

app_name = "sondaggi"

urlpatterns = (
	url(r'^$', views.index_view, name = 'index'),
	url(r'^aggiungi/$', views.create_sondaggio_view, name = "create_poll"),
	url(r'^(?P<poll_id>[0-9]+)/aggiungi_scelta/(?P<n_choices>[0-9]+)/$', views.create_choice_view,
	    name = "create_choice"),

	url(r'^(?P<poll_id>[0-9]+)/rimuovi_scelta/(?P<choice_id>[0-9]+)/$', views.delete_choice_view,
	    name = "delete_choice"),
	url(r'^(?P<poll_id>[0-9]+)/rimuovi/', views.delete_poll_view, name = "delete_poll"),

	url(r'^(?P<poll_id>[0-9]+)/aggiorna/', views.update_poll_view, name = "update_poll"),
	url(r'^(?P<poll_id>[0-9]+)/modifica_scelta/(?P<choice_id>[0-9]+)/$', views.update_choice_view,
	    name = "update_choice"),

	url(r'^(?P<poll_id>\d+)/$', views.sondaggio_view, name = 'detail'),
	url(r'^(?P<poll_id>\d+)/risultati/$', views.results_view, name = 'results'),
	url(r'^(?P<poll_id>\d+)/vota/$', views.vote, name = 'vote'),
)
