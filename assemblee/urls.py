from django.urls import path

from .views import *

app_name = "assemblee"

urlpatterns = [
	path('', all_assemblee_view, name = "all_assemblee"),
	path('<int:id_assemblea>/', assemblea_view, name = "assemblea"),
	path('<int:id_assemblea>/<int:id_turno>/', turno_view, name = "turno"),
	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/', gruppo_view, name = "gruppo"),

	path('aggiungi_assemblea/', create_assemblea_view, name = "create_assemblea"),
	path('<int:id_assemblea>/aggiungi_turno/<int:n_turni>/', create_turno_view, name = "create_turno"),
	path('<int:id_assemblea>/<int:id_turno>/aggiungi_gruppo/', create_gruppo_view,
	     name = "create_gruppo"),

	path('<int:id_assemblea>/update/', update_assemblea_view, name = "update_assemblea"),
	path('<int:id_assemblea>/<int:id_turno>/update/', update_turno_view, name = "update_turno"),
	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/update/', update_gruppo_view,
	     name = "update_gruppo"),

	path('<int:id_assemblea>/delete/', delete_assemblea_view, name = "delete_assemblea"),
	path('<int:id_assemblea>/<int:id_turno>/delete/', delete_turno_view, name = "delete_turno"),
	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/delete/', delete_gruppo_view,
	     name = "delete_gruppo"),

	path('<int:id_assemblea>/apri_iscrizioni/', apri_iscrizioni_view, name = "apri_iscrizioni"),
	path('<int:id_assemblea>/chiudi_iscrizioni/', chiudi_iscrizioni_view, name = "chiudi_iscrizioni"),
	path('<int:id_assemblea>/mostra/', mostra_assemblea_view, name = "mostra_assemblea"),
	path('<int:id_assemblea>/nascondi/', nascondi_assemblea_view, name = "nascondi_assemblea"),

	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/<int:id_utente>/disiscrivi/',
	     disiscrivi_view, name = "disiscrivi"),
	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/iscrizione/', iscrizione_view,
	     name = 'iscrizione'),
	path('<int:id_assemblea>/<int:id_turno>/<int:id_gruppo>/disiscrizione/', disiscrizione_view,
	     name = 'disiscrizione'),
]
