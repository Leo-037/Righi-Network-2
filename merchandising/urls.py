from django.contrib.auth.decorators import login_required
from django.urls import path

from merchandising.views import CreateProdotto, Index, UpdateProdotto, DeleteProdotto, Card, add_tag, remove_tag

app_name = "merchandising"
urlpatterns = [
	path('', login_required(Index.as_view()), name = 'index'),
	path('<int:pk>/edit/', login_required(UpdateProdotto.as_view()), name = 'update'),
	path('<int:pk>/delete/', login_required(DeleteProdotto.as_view()), name = 'delete'),
	path('aggiungi_prodotto/', login_required(CreateProdotto.as_view()), name = 'aggiungi_prodotto'),
	path('<int:pk>/add_tag/<str:tag>/', add_tag, name = 'add-tag'),
	path('<int:pk>/remove_tag/<str:tag>/', remove_tag, name = 'remove-tag'),
	path('galvani_card', login_required(Card.as_view()), name = 'galvani_card'),
]
