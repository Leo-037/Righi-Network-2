from django.urls import path, include

from .views import *

app_name = "assemblee"

urlpatterns = [
	path('', all_assemblee_view, name = "all_assemblee"),
	path('aggiungi_assemblea/', create_assemblea_view, name = "create_assemblea"),
	path('<int:id_assemblea>/', include([
		path('', assemblea_view, name = "assemblea"),
		path('aggiungi_turno/<int:n_turni>/', create_turno_view, name = "create_turno"),
		path('update/', update_assemblea_view, name = "update_assemblea"),
		path('delete/', delete_assemblea_view, name = "delete_assemblea"),
		path('apri_iscrizioni/', apri_iscrizioni_view, name = "apri_iscrizioni"),
		path('chiudi_iscrizioni/', chiudi_iscrizioni_view, name = "chiudi_iscrizioni"),
		path('mostra/', mostra_assemblea_view, name = "mostra_assemblea"),
		path('nascondi/', nascondi_assemblea_view, name = "nascondi_assemblea"),
		path('<int:id_turno>/', include([
			path('', turno_view, name = "turno"),
			path('aggiungi_gruppo/', create_gruppo_view, name = "create_gruppo"),
			path('update/', update_turno_view, name = "update_turno"),
			path('delete/', delete_turno_view, name = "delete_turno"),
			path('<int:id_gruppo>/', include([
				path('', gruppo_view, name = "gruppo"),
				path('update/', update_gruppo_view, name = "update_gruppo"),
				path('delete/', delete_gruppo_view, name = "delete_gruppo"),
				path('iscrizione/', iscrizione_view, name = 'iscrizione'),
				path('disiscrizione/', disiscrizione_view, name = 'disiscrizione'), ])),
			path('<int:id_utente>/disiscrivi/', disiscrivi_view, name = "disiscrivi"),
		])),
	])),
]
