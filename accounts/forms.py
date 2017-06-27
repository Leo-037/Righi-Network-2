from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.shortcuts import redirect

from .models import *

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Questo utente non esiste")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorretta")
            if not user.is_active:
                raise forms.ValidationError("Questo utente non è più attivo")
        return super(UserLoginForm, self).clean()


class Signupform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Signupform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('Aggiungi Studente', 'Aggiungi Studente', css_class='btn-primary'))
        self.helper.layout = Layout(
            'username',
            'nome',
            'cognome',
            'classe',
            'sezione',
        )

    nome = forms.CharField(label='Nome')
    cognome = forms.CharField(label='Cognome')
    classe = forms.IntegerField(min_value=1, max_value=5)
    sezione = forms.CharField(max_length=1)

    class Meta:
        model = User
        fields = [
            'username',
            'nome',
            'cognome',
            'classe',
            'sezione',
        ]

    def clean_sezione(self):
        sezione = self.cleaned_data.get('sezione')
        sezione.upper()
        return sezione

    def signup(self, request, user):
        user.first_name = self.cleaned_data["nome"]
        user.last_name = self.cleaned_data["cognome"]
        user.save()
        classe = self.cleaned_data["classe"]
        sezione = self.cleaned_data["sezione"]
        stud = Studente(user=user, classe=classe, sezione=sezione, is_attivato=True)
        stud.save()
        return redirect("/")


class ClasseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClasseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(Div(
            'classe',
            'sezione',
            Submit('Aggiungi Classe', 'Aggiungi Classe', css_class='btn-primary')
        ))

    classe = forms.IntegerField(min_value=1, max_value=5)
    sezione = forms.CharField(max_length=1)

    def clean_sezione(self):
        sezione = self.cleaned_data.get('sezione')
        sezione.upper()
        return sezione
