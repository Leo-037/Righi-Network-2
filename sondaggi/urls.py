from django.urls import path, include

from . import views

app_name = "sondaggi"

urlpatterns = (
	path('', views.index_view, name = 'index'),
	path('aggiungi/', views.create_sondaggio_view, name = "create_poll"),
	path('<int:poll_id>/', include([
		path('', views.sondaggio_view, name = 'detail'),
		path('aggiorna/', views.update_poll_view, name = "update_poll"),
		path('aggiungi_scelta/<int:n_choices>/', views.create_choice_view, name = "create_choice"),
		path('modifica_scelta/<int:choice_id>/', views.update_choice_view, name = "update_choice"),
		path('rimuovi_scelta/<int:choice_id>/', views.delete_choice_view, name = "delete_choice"),
		path('rimuovi/', views.delete_poll_view, name = "delete_poll"),
		path('risultati/', views.results_view, name = 'results'),
		path('vota/', views.vote, name = 'vote'),
	])),
)
