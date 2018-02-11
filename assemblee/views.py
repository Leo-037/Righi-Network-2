from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import *


# CREATE

@login_required
def create_assemblea_view(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		if request.method == "GET":
			form = AssembleaForm(initial = {'n_turni': 0})
			return render(request, 'assemblee/assemblea_form.html', {'title': "Crea Assemblea", 'form': form})
		elif request.method == "POST":
			form = AssembleaForm(request.POST)
			if form.is_valid():
				n_turni = form.cleaned_data['n_turni']
				assemblea = form.save()
				if n_turni >= 1:
					return redirect("assemblee:create_turno", assemblea.id, n_turni)
				return redirect("assemblee:assemblea", assemblea.id)
	raise Http404


@login_required
def create_turno_view(request, id_assemblea, n_turni):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		if request.method == "GET":
			assemblea = Assemblea.objects.get(id = id_assemblea)
			form = TurnoForm(initial = {'assemblea': assemblea})
			form.fields['assemblea'].widget = forms.HiddenInput()
			return render(request, 'assemblee/turno_form.html',
			              {'title': "Aggiungi Turno", 'form': form, 'assemblea': assemblea})
		elif request.method == "POST":
			form = TurnoForm(request.POST)
			form.save()

			n_turni = int(n_turni)
			if n_turni > 1:
				n_turni -= 1
				return redirect("assemblee:create_turno", id_assemblea, n_turni)
			return redirect("assemblee:assemblea", id_assemblea)
	raise Http404


@login_required
def create_gruppo_view(request, id_assemblea, id_turno):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		if request.method == "GET":
			turno = Turno.objects.get(id = id_turno)
			form = GruppoForm(initial = {'turno': turno})
			form.fields['turno'].widget = forms.HiddenInput()
			return render(request, 'assemblee/gruppo_form.html',
			              {'title': "Aggiungi Gruppo", 'turno': turno, 'form': form})
		elif request.method == "POST":
			form = GruppoForm(request.POST)
			form.save()

			turno = Turno.objects.get(id = id_turno)
			return redirect("assemblee:turno", id_assemblea, turno.id)
	raise Http404


# RETRIEVE

@login_required
def all_assemblee_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	assemblee = Assemblea.objects.filter().order_by("-data", "-id")
	context = {
		'assemblee': assemblee,
		'today': timezone.now().date(),
		'title': "Assemblee",
	}
	return render(request, 'assemblee/assemblee.html', context)


@login_required
def assemblea_view(request, id_assemblea):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		raise Http404

	turni = Turno.objects.filter(assemblea = assemblea).order_by("inizio")

	context = {
		"title": f"Assemblea {assemblea.data}",
		'assemblea': assemblea,
		'turni': turni,
		'today': timezone.now().date(),
	}
	return render(request, 'assemblee/assemblea.html', context)


@login_required
def turno_view(request, id_assemblea, id_turno):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		raise Http404

	turno = Turno.objects.get(id = id_turno)
	gruppi = Gruppo.objects.filter(turno = turno)
	gruppo_iscritto = None

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			gruppo_iscritto = gruppo

	context = {
		'turno': turno,
		'gruppi': gruppi,
		'gruppo_iscritto': gruppo_iscritto,
		'title': "Turno delle " + str(turno.inizio.strftime("%H:%M")),
	}

	return render(request, 'assemblee/turno.html', context)


@login_required
def gruppo_view(request, id_assemblea, id_turno, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		raise Http404

	gruppo = Gruppo.objects.get(id = id_gruppo)

	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__user__last_name")

	gruppo_iscritto = False
	if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
		gruppo_iscritto = True

	if request.method == "POST":
		da_discrivere = request.POST.getlist('iscritto_da_cancellare')
		for id in da_discrivere:
			iscritto = Iscritto.objects.get(id = id)
			gruppo.iscritti -= 1
			iscritto.delete()
			gruppo.save()

	context = {
		'title': gruppo.titolo,
		'gruppo': gruppo,
		'gruppo_iscritto': gruppo_iscritto,
		'iscritti': iscritti
	}

	return render(request, 'assemblee/gruppo.html', context)


# UPDATE

@login_required
def update_assemblea_view(request, id_assemblea):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	assemblea = get_object_or_404(Assemblea, id = id_assemblea)
	form = AssembleaForm(request.POST or None, request.FILES or None, instance = assemblea, initial = {'n_turni': 0})
	form.fields['n_turni'].widget = forms.HiddenInput()
	if form.is_valid():
		assemblea = form.save(commit = False)
		assemblea.save()
		messages.success(request, "Assemblea salvata", extra_tags = 'html_safe')
		return redirect("assemblee:assemblea", id_assemblea)

	context = {
		"title": "Modifica assemblea",
		"assemblea": assemblea,
		"form": form,
	}
	return render(request, "assemblee/assemblea_form.html", context)


@login_required
def update_turno_view(request, id_assemblea, id_turno):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	assemblea = Assemblea.objects.get(id = id_assemblea)
	turno = get_object_or_404(Turno, id = id_turno)
	form = TurnoForm(request.POST or None, request.FILES or None, instance = turno,
	                 initial = {'assemblea': turno.assemblea})
	form.fields['assemblea'].widget = forms.HiddenInput()
	if form.is_valid():
		turno = form.save(commit = False)
		turno.save()
		messages.success(request, "Turno salvato", extra_tags = 'html_safe')
		return redirect("assemblee:turno", id_assemblea, turno.id)

	context = {
		"title": "Modifica turno",
		"assemblea": assemblea,
		"turno": turno,
		"form": form,
	}
	return render(request, "assemblee/turno_form.html", context)


@login_required
def update_gruppo_view(request, id_assemblea, id_turno, id_gruppo):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	gruppo = get_object_or_404(Gruppo, id = id_gruppo)
	form = GruppoForm(request.POST or None, request.FILES or None, instance = gruppo,
	                  initial = {'turno': gruppo.turno})
	form.fields['turno'].widget = forms.HiddenInput()
	if form.is_valid():
		gruppo = form.save(commit = False)
		gruppo.save()
		messages.success(request, "Gruppo salvato", extra_tags = 'html_safe')
		return redirect(
			"assemblee:turno", id_assemblea = id_assemblea, id_turno = id_turno)

	context = {
		"title": "Modifica gruppo",
		"gruppo": gruppo,
		'turno': gruppo.turno,
		"form": form,
	}
	return render(request, "assemblee/gruppo_form.html", context)


# DELETE

@login_required
def delete_assemblea_view(request, id_assemblea):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.delete()
		messages.success(request, "Cancellato", extra_tags = 'html_safe')
		return redirect("assemblee:all_assemblee")
	raise Http404


@login_required
def delete_turno_view(request, id_assemblea, id_turno):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		turno = Turno.objects.get(id = id_turno)
		turno.delete()
		messages.success(request, "Cancellato", extra_tags = 'html_safe')
		return redirect("assemblee:assemblea", id_assemblea)
	raise Http404


@login_required
def delete_gruppo_view(request, id_assemblea, id_turno, id_gruppo):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		gruppo.delete()
		messages.success(request, "Cancellato", extra_tags = 'html_safe')
		return redirect("assemblea:turno", id_assemblea, id_turno)
	raise Http404


# STRUMENTI

@login_required
def apri_iscrizioni_view(request, id_assemblea):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.iscrizioni_aperte = True
		assemblea.save()
		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("assemblee:all_assemblee")
	raise Http404


@login_required
def chiudi_iscrizioni_view(request, id_assemblea):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.iscrizioni_aperte = False
		assemblea.save()
		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("assemblee:all_assemblee")
	raise Http404


@login_required
def mostra_assemblea_view(request, id_assemblea):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.mostra = True
		assemblea.save()
		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("assemblee:all_assemblee")
	raise Http404


@login_required
def nascondi_assemblea_view(request, id_assemblea):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		assemblea = Assemblea.objects.get(id = id_assemblea)
		assemblea.mostra = False
		assemblea.iscrizioni_aperte = False
		assemblea.save()
		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("assemblee:all_assemblee")
	raise Http404


# ISCRITTI


@login_required
def iscrizione_view(request, id_assemblea, id_turno, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		if not assemblea.iscrizioni_aperte:
			raise Http404

	turno = Turno.objects.get(id = id_turno)

	for gruppo in Gruppo.objects.filter(turno = turno):
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo):
			Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo).delete()
			gruppo.iscritti -= 1
			gruppo.save()

	gruppo = Gruppo.objects.get(id = id_gruppo)
	if not gruppo.iscritti == gruppo.iscritti_massimi:
		iscritto = Iscritto(studente = request.user.studente, gruppo = gruppo)
		gruppo.iscritti += 1
		iscritto.save()
		gruppo.save()

		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("assemblee:turno", id_assemblea, id_turno)
	raise Http404


@login_required
def disiscrizione_view(request, id_assemblea, id_turno, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		if not assemblea.iscrizioni_aperte:
			raise Http404

	gruppo = Gruppo.objects.get(id = id_gruppo)
	iscritto = Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo)
	gruppo.iscritti -= 1
	iscritto.delete()
	gruppo.save()

	next = request.GET.get("next")
	if next:
		return redirect(next)
	return redirect("assemblee:turno", id_assemblea, id_turno)


@login_required
def disiscrivi_view(request, id_assemblea, id_turno, id_gruppo, id_utente):
	if not request.user.studente.is_attivato:
		raise Http404

	assemblea = Assemblea.objects.get(id = id_assemblea)
	if not assemblea.mostra and not (request.user.studente.is_rapistituto or request.user.is_superuser):
		if not assemblea.iscrizioni_aperte:
			raise Http404

	if request.user.studente.is_rapistituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		utente = User.objects.get(id = id_utente)
		iscritto = Iscritto.objects.get(studente = utente.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		return redirect("assemblee:gruppo", id_assemblea, id_turno, id_gruppo)
	else:
		raise Http404
