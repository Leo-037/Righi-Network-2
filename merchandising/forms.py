from django import forms
from taggit.forms import TagField

from merchandising.models import Prodotto


class ProdottoForm(forms.ModelForm):
	tags = TagField(required = False)

	class Meta:
		model = Prodotto
		fields = ['nome', 'descrizione', 'foto', 'costo', 'tags']
