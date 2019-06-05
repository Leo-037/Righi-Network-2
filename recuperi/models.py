from django import forms
from django.db import models
from django.forms import ModelForm

from accounts.models import Studente


class Settimana(models.Model):
	iscrizioni_aperte = models.BooleanField(default = False)


class Gruppo(models.Model):
	titolo = models.TextField(blank = True, null = True)
	aula = models.TextField(blank = True, null = True)
	descrizione = models.TextField(default = "", blank = True, null = True)
	host = models.TextField(verbose_name = "Tenuto da ")

	prima = models.BooleanField(default = False)
	seconda = models.BooleanField(default = False)
	terza = models.BooleanField(default = False)
	quarta = models.BooleanField(default = False)
	quinta = models.BooleanField(default = False)

	lunedi = models.BooleanField(default = False)
	martedi = models.BooleanField(default = False)
	mercoledi = models.BooleanField(default = False)
	giovedi = models.BooleanField(default = False)
	venerdi = models.BooleanField(default = False)

	iscritti_massimi = models.PositiveIntegerField(default = 20)
	iscritti = models.PositiveIntegerField(default = 0)


class Iscritto(models.Model):
	studente = models.ForeignKey(Studente, on_delete = models.CASCADE, related_name = "iscritti_recuperi")
	gruppo = models.ForeignKey(Gruppo, on_delete = models.CASCADE)


class GruppoForm(ModelForm):
	class Meta:
		model = Gruppo
		text_widget = forms.TextInput()
		exclude = ('iscritti',)
		widgets = {
			'aula': text_widget,
			'titolo': text_widget,
			'host': text_widget,
		}


class IscrittoForm(ModelForm):
	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
