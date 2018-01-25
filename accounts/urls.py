from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
	path('', views.classi_view, name = 'gestione'),
	path('ospiti/', include([
		path('', views.guests_view, name = "guests"),
		path('aggiungi-ospite/', views.aggiungi_ospite_view, name = 'add-guest'),
	])),
	path('<str:classe>-<str:sezione>/', include([
		path('', views.dettagli_classe_view, name = 'classe'),
	])),
	path('elimina_studente/<str:username>/', views.elimina_studente_view, name = "delete-user"),
	path('elimina_dummy/<str:username>/', views.elimina_dummy_view, name = "delete-dummy"),
	path('elimina_ospite/<str:username>/', views.elimina_ospite_view, name = "delete-guest"),
	path('modifica_studente/<str:username>/', views.edit_studente_view, name = "edit-user"),
]
