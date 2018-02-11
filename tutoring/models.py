from django.db import models
from django.forms import ModelForm

from accounts.models import Studente


class Tutor(models.Model):
	studente = models.ForeignKey(Studente, models.CASCADE)

	materia = models.CharField(max_length = 15)

	n_studenti = models.PositiveIntegerField(default = 0)

	prima = models.BooleanField(default = True)
	seconda = models.BooleanField(default = True)
	terza = models.BooleanField(default = True)
	quarta = models.BooleanField(default = True)
	quinta = models.BooleanField(default = True)

	approvato = models.BooleanField(default = False)

	cellulare = models.PositiveIntegerField(verbose_name = "Numero di cellulare")


class Allievo(models.Model):
	tutor = models.ForeignKey(Tutor, models.CASCADE)
	studente = models.ForeignKey(Studente, models.CASCADE)


class TutorForm(ModelForm):
	class Meta:
		model = Tutor

		fields = ['materia', 'cellulare', 'prima', 'seconda', 'terza', 'quarta', 'quinta']

	def clean_materia(self):
		materia = self.cleaned_data.get("materia")
		materia.lower()
		return materia
