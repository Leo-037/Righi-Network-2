from django.conf.urls import url

from .views import *

app_name = "assemblee"

urlpatterns = [
	url(r'^$', all_assemblee_view, name = "all_assemblee"),
	url(r'^(?P<id_assemblea>[0-9]+)/$', assemblea_view, name = "assemblea"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/$', turno_view, name = "turno"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/$', gruppo_view, name = "gruppo"),

	url(r'^aggiungi_assemblea/$', create_assemblea_view, name = "create_assemblea"),
	url(r'^(?P<id_assemblea>[0-9]+)/aggiungi_turno/(?P<n_turni>[0-9]+)/$', create_turno_view, name = "create_turno"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/aggiungi_gruppo/$', create_gruppo_view,
	    name = "create_gruppo"),

	url(r'^(?P<id_assemblea>[0-9]+)/update/$', update_assemblea_view, name = "update_assemblea"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/update/$', update_turno_view, name = "update_turno"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/update/$', update_gruppo_view,
	    name = "update_gruppo"),

	url(r'^(?P<id_assemblea>[0-9]+)/delete/$', delete_assemblea_view, name = "delete_assemblea"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/delete/$', delete_turno_view, name = "delete_turno"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/delete/$', delete_gruppo_view,
	    name = "delete_gruppo"),

	url(r'(?P<id_assemblea>[0-9]+)/apri_iscrizioni/', apri_iscrizioni_view, name = "apri_iscrizioni"),
	url(r'(?P<id_assemblea>[0-9]+)/chiudi_iscrizioni/', chiudi_iscrizioni_view, name = "chiudi_iscrizioni"),
	url(r'(?P<id_assemblea>[0-9]+)/mostra/', mostra_assemblea_view, name = "mostra_assemblea"),
	url(r'(?P<id_assemblea>[0-9]+)/nascondi/', nascondi_assemblea_view, name = "nascondi_assemblea"),

	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/(?P<id_utente>[0-9]+)/disiscrivi/',
	    disiscrivi_view, name = "disiscrivi"),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/iscrizione/', iscrizione_view,
	    name = 'iscrizione'),
	url(r'^(?P<id_assemblea>[0-9]+)/(?P<id_turno>[0-9]+)/(?P<id_gruppo>[0-9]+)/disiscrizione/', disiscrizione_view,
	    name = 'disiscrizione'),
]
