from django.urls import path, include

from .views import *

app_name = "recuperi"

urlpatterns = [
	path('', recuperi_view, name = "main"),
	path('apri_iscrizioni/', apri_iscrizioni_view, name = "apri_iscrizioni"),
	path('chiudi_iscrizioni/', chiudi_iscrizioni_view, name = "chiudi_iscrizioni"),
	path('aggiungi_gruppo/', create_gruppo_view, name = "create_gruppo"),
	path('<int:id_gruppo>/', include([
		path('', gruppo_view, name = "gruppo"),
		path('update/', update_gruppo_view, name = "update_gruppo"),
		path('delete/', delete_gruppo_view, name = "delete_gruppo"),
		path('iscrizione/', iscrizione_view, name = 'iscrizione'),
		path('disiscrizione/', disiscrizione_view, name = 'disiscrizione'),
		path('stampa/', pdf_iscritti_view, name = 'stampa_iscritti'),
		path('<int:id_utente>/disiscrivi/', disiscrivi_view, name = "disiscrivi"),
	])),
]
