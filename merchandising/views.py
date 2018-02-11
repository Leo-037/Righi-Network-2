from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from merchandising.models import Prodotto


def all_tags():
	tags = []
	for post in Prodotto.objects.all():
		tags += post.tags.all()
	tags = list(set(tags))
	return tags


def add_tag(request, pk, tag = None):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	object = get_object_or_404(Prodotto, pk = pk)
	object.tags.add(tag)

	return redirect("merchandising:index")


def remove_tag(request, pk, tag):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	object = get_object_or_404(Prodotto, pk = pk)
	object.tags.remove(tag)

	return redirect("merchandising:index")


class CreateProdotto(CreateView):
	model = Prodotto
	fields = ['nome', 'descrizione', 'foto', 'costo']
	# form_class = ProdottoForm

	title = "Aggiungi prodotto"
	success_url = reverse_lazy('merchandising:index')
	template_name = "merchandising/prodotto_form.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context


class UpdateProdotto(UpdateView):
	model = Prodotto
	fields = ['nome', 'descrizione', 'foto', 'costo']
	title = "Modifica prodotto"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context


class DeleteProdotto(DeleteView):
	model = Prodotto
	success_url = reverse_lazy('merchandising:index')

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)


class Index(ListView):
	title = "Merchandising"
	template_name = "merchandising/index.html"
	model = Prodotto

	paginate_by = 25

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		context['tags'] = all_tags()
		return context

	def get_queryset(self):
		queryset = Prodotto.objects.all()

		query = self.request.GET.get("q")
		next = self.request.GET.get("next")
		tag = self.request.GET.get("tag")

		if query:
			queryset = queryset.filter(
				Q(nome__icontains = query) |
				Q(descrizione__icontains = query) |
				Q(costo__icontains = query)
			).distinct()

		if tag:
			queryset = queryset.filter(tags__name__in = [tag])

		return queryset


class Card(TemplateView):
	template_name = "merchandising/galvani_card.html"
