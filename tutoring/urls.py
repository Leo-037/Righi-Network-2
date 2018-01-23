from django.urls import path

from .views import list_tutors, tutor_form_view, richiedi_tutor, approva_tutor, elimina_tutor, gestione_tutor

app_name = "tutoring"
urlpatterns = [
	path('', list_tutors, name = "index"),
	path('richiedi-tutor/<int:pk>/', richiedi_tutor, name = "chiedi_tutor"),
	path('diventa-tutor/', tutor_form_view, name = "diventa-tutor"),
	path('gestione/', gestione_tutor, name = "gestione"),
	path('gestione/approva-tutor/<int:pk>/', approva_tutor, name = "approva-tutor"),
	path('gestione/elimina-tutor/<int:pk>/', elimina_tutor, name = "delete"),
]
