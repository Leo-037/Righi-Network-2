import random

from django.contrib.auth import (
	authenticate,
	get_user_model,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404

from .forms import GuestRegisterForm, StudenteRegisterForm, DummySignupForm
from .models import Studente, DummyUser, Guest

User = get_user_model()


@login_required()
def change_color_view(request, colore):
	studente = request.user.studente
	studente.colore = colore
	studente.save()
	return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def guests_view(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		ospiti = Guest.objects.all()

		if request.method == "GET":
			form = GuestRegisterForm()

			return render(request, 'account/righinetwork/lista_ospiti.html',
			              {'form': form, 'ospiti': ospiti})

		elif request.method == "POST":
			form = GuestRegisterForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']

				new_password = generate_password(8)

				new_user = User(username = username)
				new_user.set_password(new_password)
				new_user.save()

				user = authenticate(username = username, password = new_password)

				ospite = Guest(user = user, password = new_password)
				ospite.save()

				return redirect("/")
	else:
		return Http404


@login_required()
def aggiungi_ospite_view(request):
	context = {}
	return render(request, "account/righinetwork/guest_form.html", context)


def signup_view(request):
	form = DummySignupForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["otpassword"]
		new_password = form.cleaned_data["new_password"]
		email = form.cleaned_data["email"]

		dummy = DummyUser.objects.get(username = username)

		nome = dummy.first_name
		cognome = dummy.last_name

		new_user = User(username = username, first_name = nome, last_name = cognome, email = email)
		new_user.set_password(new_password)
		new_user.save()

		user = authenticate(username = username, password = new_password)

		studente = dummy.studente
		studente.user = user
		studente.is_attivato = True
		studente.save()

		dummy.delete()

		return redirect("/")

	return render(request, 'account/signup.html',
	              {'form': form, 'redirect_field_name': "/", "login_url": "accounts/login"})


@login_required()
def classi_view(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		studenti = Studente.objects.all()

		classi = [1, 2, 3, 4, 5]
		sezioni = []

		classi_complete = []

		for studente in studenti:
			sezione = studente.sezione
			if sezione not in sezioni:
				sezioni.append(sezione)
				sezioni.sort()

		for classe in classi:
			for sezione in sezioni:
				if len(Studente.objects.filter(classe = classe, sezione = sezione)) > 0:
					classe_completa = (classe, sezione)
					classi_complete.append(classe_completa)

		studenti_totali = len(Studente.objects.all())
		studenti_attivati = len(Studente.objects.filter(is_attivato = True))
		ospiti = len(Guest.objects.all())

		return render(request, "account/righinetwork/classi.html",
		              {'classi': classi_complete, 'studenti_attivati': studenti_attivati,
		               'studenti_totali': studenti_totali, 'ospiti': ospiti})
	else:
		raise Http404


@login_required()
def dettagli_classe_view(request, classe, sezione):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		sezione = sezione.upper()
		studenti_attivi = Studente.objects.filter(classe = classe, sezione = sezione, is_attivato = True).order_by(
			"user__last_name", "user__first_name")
		studenti_inattivi = DummyUser.objects.filter(studente__classe__exact = classe,
		                                             studente__sezione__exact = sezione).order_by("last_name",
		                                                                                          "first_name")

		if request.method == "GET":
			form = StudenteRegisterForm()

			return render(request, 'account/righinetwork/dettagli_classe.html',
			              {'form': form, 'classe': classe, 'sezione': sezione, 'studenti_attivi': studenti_attivi,
			               'studenti_inattivi': studenti_inattivi})

		elif request.method == "POST":
			form = StudenteRegisterForm(request.POST)
			print(form.is_valid())
			if form.is_valid():
				print("Valido!")

				nome = form.cleaned_data['nome']
				cognome = form.cleaned_data['cognome']
				username = clean_username(nome, cognome)
				password = generate_password(8)

				studente = Studente(classe = classe, sezione = sezione.upper(),
				                    otpassword = password)
				studente.save()

				dummy = DummyUser(username = username, first_name = nome, last_name = cognome, otpassword = password,
				                  studente = studente)
				dummy.save()

			return redirect("/gestione/" + str(classe) + "-" + str(sezione) + "/")


	else:
		raise Http404


def clean_username(nome, cognome):
	newusername = nome + "_" + cognome
	newusername = newusername.lower()
	newusername = newusername.replace(" ", "_")
	newusername = newusername.replace("à", "a")
	newusername = newusername.replace("è", "e")
	newusername = newusername.replace("ì", "i")
	newusername = newusername.replace("ò", "o")
	newusername = newusername.replace("ù", "u")
	while len(User.objects.filter(username = newusername)) != 0:
		pezzi = newusername.split("_")
		numero = pezzi[-1]
		if numero.isdigit():
			del pezzi[-1]

			numero = int(numero) + 1
			pezzi.append(numero)
			newusername = ""
			for pezzo in pezzi:
				newusername += str(pezzo) + "_"
			newusername = newusername[:-1]
		else:
			newusername += "_1"

	return newusername


def generate_password(length):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	upperalphabet = alphabet.upper()
	pw_len = length
	pwlist = []

	for i in range(pw_len // 3):
		pwlist.append(alphabet[random.randrange(len(alphabet))])
		pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
		pwlist.append(str(random.randrange(10)))
	for i in range(pw_len - len(pwlist)):
		pwlist.append(alphabet[random.randrange(len(alphabet))])

	random.shuffle(pwlist)
	pwstring = "".join(pwlist)

	return pwstring


@login_required()
def elimina_studente_view(request, username):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		user = User.objects.get(username = username)
		studente = Studente.objects.get(user = user)
		studente.delete()
		user.delete()
		url = request.get_full_path()[:14]
		return redirect(url)
	else:
		raise Http404


@login_required()
def elimina_dummy_view(request, username):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		dummy = DummyUser.objects.get(username = username)
		studente = dummy.studente
		studente.delete()
		dummy.delete()
		url = request.get_full_path()[:14]
		return redirect(url)
	else:
		raise Http404


@login_required()
def elimina_ospite_view(request, username):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		user = User.objects.get(username = username)
		ospite = Guest.objects.get(user = user)
		ospite.delete()
		user.delete()
		return redirect("accounts:guests")
	else:
		raise Http404
