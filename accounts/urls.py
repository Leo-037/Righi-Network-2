from django.conf.urls import url, include

from . import views

app_name = "accounts"

urlpatterns = [
    url(r'^$', views.classi_view, name='gestione'),
    url(r'^ospiti/', include([
        url(r'^$', views.guests_view, name="guests"),
        url(r'^aggiungi-ospite$', views.aggiungi_ospite_view, name='add-guest'),
    ])),
    url(r'^(?P<classe>[\w-])-(?P<sezione>[\w-])/', include([
        url(r'^$', views.dettagli_classe_view, name='classe'),
    ])),
    url(r"^elimina_studente/(?P<username>['\w-]+)/$", views.elimina_studente_view, name="delete-user"),
    url(r"^elimina_dummy/(?P<username>['\w-]+)/$", views.elimina_dummy_view, name="delete-dummy"),
    url(r"^elimina_ospite/(?P<username>['\w-]+)/$", views.elimina_ospite_view, name="delete-guest"),

]
