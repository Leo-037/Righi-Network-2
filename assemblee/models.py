from django import forms
from django.db import models
from django.forms import ModelForm

from accounts.models import Studente


# Create your models here.

class Assemblea(models.Model):
	data = models.DateField()
	sede = models.CharField(max_length = 150, choices = (("Sede", "Sede"), ("Succursale", "Succursale")))
	mostra = models.BooleanField(default = False)
	iscrizioni_aperte = models.BooleanField(default = False)


class Turno(models.Model):
	inizio = models.TimeField(verbose_name = "Orario di inizio")
	fine = models.TimeField(verbose_name = "Fine turno")
	assemblea = models.ForeignKey(Assemblea, on_delete = models.CASCADE)


class Gruppo(models.Model):
	titolo = models.TextField()
	aula = models.TextField()
	descrizione = models.TextField()
	host = models.TextField(verbose_name = "Tenuto da ")

	iscritti_massimi = models.PositiveIntegerField()
	iscritti = models.PositiveIntegerField(default = 0)

	turno = models.ForeignKey(Turno, on_delete = models.CASCADE)


class Iscritto(models.Model):
	studente = models.ForeignKey(Studente, on_delete = models.CASCADE, related_name = "iscritti_assemblee")
	gruppo = models.ForeignKey(Gruppo, on_delete = models.CASCADE)


class AssembleaForm(ModelForm):
	n_turni = forms.IntegerField(label = "Numero turni", min_value = 0, )

	class Meta:
		model = Assemblea
		data_widget = forms.SelectDateWidget()

		fields = ['sede', 'data', 'n_turni']
		widgets = {
			'data': data_widget,
		}


class TurnoForm(ModelForm):
	class Meta:
		model = Turno
		ora_widget = forms.TimeInput()

		fields = ['inizio', 'fine', 'assemblea']
		widgets = {
			'inizio': ora_widget,
			'fine': ora_widget,
		}


class GruppoForm(ModelForm):
	class Meta:
		model = Gruppo
		text_widget = forms.TextInput()
		fields = ['aula', 'titolo', 'descrizione', 'host', 'iscritti_massimi', 'turno']
		widgets = {
			'aula': text_widget,
			'titolo': text_widget,
			'host': text_widget,
		}


class IscrittoForm(ModelForm):
	class Meta:
		model = Iscritto
		fields = ['studente', 'gruppo']
