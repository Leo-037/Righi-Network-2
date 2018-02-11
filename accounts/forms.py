from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
)
from django.utils.translation import ugettext_lazy as _

from .models import DummyUser

User = get_user_model()


class UserLoginForm(LoginForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.error_messages = {
			'account_inactive':
				_("Questo account al momento è inattivo"),

			'email_password_mismatch':
				_("L'indirizo email e/o la password non sono corretti"),

			'username_password_mismatch':
				_("L'username e/o la password non sono corretti"),
		}

	def clean(self, *args, **kwargs):
		super(UserLoginForm, self).clean()
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Questo utente non esiste")
			if not user.check_password(password):
				raise forms.ValidationError("Password Incorretta")
			if not user.is_active:
				raise forms.ValidationError("Questo utente non è più attivo")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class StudenteRegisterForm(forms.Form):
	nome = forms.CharField(label = 'Nome')
	cognome = forms.CharField(label = 'Cognome')


class DummySignupForm(forms.ModelForm):
	username = forms.CharField()
	otpassword = forms.CharField(label = "Password di primo login (fornita dai rappresentanti)")
	new_password = forms.CharField(widget = forms.PasswordInput, label = "Nuova password")
	new_password2 = forms.CharField(widget = forms.PasswordInput, label = 'Conferma nuova password')
	email = forms.EmailField(label = 'Indirizzo Email')
	email2 = forms.EmailField(label = 'Conferma Email')

	class Meta:
		model = DummyUser
		exclude = ["first_name", "last_name", "studente"]

	def clean_username(self):
		username = self.cleaned_data.get("username")
		dummyusers = DummyUser.objects.filter(username = username)
		if len(dummyusers) > 0:
			return username
		else:
			raise forms.ValidationError("Utente inesistente")

	def clean_otpassword(self):
		otpassword_form = self.cleaned_data.get("otpassword")
		username = self.cleaned_data.get("username")
		self.clean_username()
		otpassword_model = DummyUser.objects.get(username = username).otpassword
		if otpassword_form != otpassword_model:
			raise forms.ValidationError("Password di primo login non valida")
		return otpassword_form

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Le mail devono coincidere")
		email_qs = User.objects.filter(email = email)
		if email_qs.exists():
			raise forms.ValidationError("Questa email è già stata registrata")
		return email

	def clean_new_password2(self):
		password = self.cleaned_data.get('new_password')
		password2 = self.cleaned_data.get('new_password2')
		if password != password2:
			raise forms.ValidationError("Le password devono coincidere")
		return password


class GuestRegisterForm(forms.Form):
	username = forms.CharField(label = 'Username')
