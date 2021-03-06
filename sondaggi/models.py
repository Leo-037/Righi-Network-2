from django import forms
from django.db import models
from django.forms import ModelForm

from accounts.models import Studente


class Poll(models.Model):
	question = models.CharField("Domanda", max_length = 200)
	timestamp = models.DateTimeField("Data", auto_now = False, auto_now_add = True)
	rapp_classe = models.BooleanField("Chiuso ai rappresentanti", default = False)

	def __str__(self):
		return self.question


class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete = models.CASCADE)
	choice_text = models.CharField("Scelta", max_length = 200)
	votes = models.PositiveIntegerField("Voti", default = 0)

	def __str__(self):
		return self.choice_text


class Vote(models.Model):
	choice = models.ForeignKey(Choice, models.CASCADE)
	studente = models.ForeignKey(Studente, models.CASCADE)


class PollForm(ModelForm):
	question = forms.CharField(max_length = 200)
	n_choices = forms.IntegerField(label = "Numero scelte", min_value = 0, )
	rapp_classe = forms.BooleanField(required = False, initial = False)

	class Meta:
		model = Poll

		fields = [
			"question",
			"n_choices",
			"rapp_classe",
		]


class ChoiceForm(ModelForm):
	class Meta:
		model = Choice

		fields = [
			"poll",
			"choice_text",
		]
