from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from .models import *


@login_required
def index_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	polls = Poll.objects.all().order_by("-timestamp")
	poll_votati = []
	for poll in polls:
		if len(Vote.objects.filter(choice__poll = poll, studente = request.user.studente)) > 0:
			poll_votati.append(poll)

	context = {
		"title": "Sondaggi",
		"polls": polls,
		"poll_votati": poll_votati,
	}
	return render(request, "sondaggi/index.html", context)


@login_required
def sondaggio_view(request, poll_id):
	if not request.user.studente.is_attivato:
		raise Http404
	poll = Poll.objects.get(id = poll_id)
	if len(Vote.objects.filter(choice__poll = poll, studente = request.user.studente)) > 0:
		return redirect("sondaggi:results", poll_id)

	choices = Choice.objects.filter(poll = poll)

	context = {
		"title": poll.question,
		"poll": poll,
		"choices": choices,
	}
	return render(request, "sondaggi/detail.html", context)


@login_required
def results_view(request, poll_id):
	if not request.user.studente.is_attivato:
		raise Http404
	poll = Poll.objects.get(id = poll_id)
	choices = Choice.objects.filter(poll = poll)
	n_voti = []
	for choice in choices:
		n_voti.append(choice.votes)
	voti_tot = sum(n_voti)

	context = {
		"title": poll.question,
		"poll": poll,
		"choices": choices,
		"voti_tot": voti_tot,
	}
	return render(request, "sondaggi/results.html", context)


@login_required
def vote(request, poll_id):
	poll = get_object_or_404(Poll, pk = poll_id)
	try:
		selected_choice = poll.choice_set.get(pk = request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'sondaggi/detail.html', {
			'poll': poll,
			'error_message': "Non hai selezionato alcuna opzione.",
		})
	else:
		if len(Vote.objects.filter(choice = selected_choice, studente = request.user.studente)) == 0:
			new_vote = Vote(choice = selected_choice, studente = request.user.studente)
			new_vote.save()
			selected_choice.votes += 1
			selected_choice.save()
			return redirect('sondaggi:results', poll.id)
		raise Http404


@login_required
def create_sondaggio_view(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		form = PollForm(request.POST or None)
		if form.is_valid():
			n_choices = form.cleaned_data['n_choices']
			messages.success(request, "Sondaggio Aggiunto")
			poll = form.save()
			if n_choices >= 1:
				return redirect("sondaggi:create_choice", poll.id, n_choices)
			return redirect('sondaggi:detail', poll.id)

		context = {
			'title': "Aggiungi sondaggio",
			"form": form,
		}
		return render(request, "sondaggi/poll_form.html", context)
	else:
		raise Http404


@login_required
def create_choice_view(request, poll_id, n_choices):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		poll = Poll.objects.get(id = poll_id)
		form = ChoiceForm(request.POST or None, initial = {'poll': poll, "votes": 0})
		form.fields['poll'].widget = forms.HiddenInput()
		if form.is_valid():
			messages.success(request, "Scelta Aggiunta")
			choice = form.save()
			n_choices = int(n_choices)
			if n_choices > 1:
				n_choices -= 1
				return redirect("sondaggi:create_choice", poll.id, n_choices)
			return redirect('sondaggi:detail', poll.id)

		context = {
			'title': 'Aggiungi scelta',
			'form': form,
			"poll": poll,
		}
		return render(request, "sondaggi/choice_form.html", context)
	else:
		raise Http404


@login_required
def delete_poll_view(request, poll_id):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		poll = Poll.objects.get(id = poll_id)
		poll.delete()
		return redirect("sondaggi:index")
	else:
		raise Http404


@login_required
def update_poll_view(request, poll_id):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		poll = Poll.objects.get(id = poll_id)
		form = PollForm(request.POST or None, instance = poll, initial = {'n_choices': 0})
		form.fields['n_choices'].widget = forms.HiddenInput()
		if form.is_valid():
			messages.success(request, "Sondaggio Modificato")
			poll = form.save()
			return redirect('sondaggi:detail', poll.id)

		context = {
			'title': 'Modifica sondaggio',
			"form": form,
		}
		return render(request, "sondaggi/poll_form.html", context)
	else:
		raise Http404


@login_required
def update_choice_view(request, poll_id, choice_id):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		poll = Poll.objects.get(id = poll_id)
		choice = Choice.objects.get(id = choice_id)
		form = ChoiceForm(request.POST or None, instance = choice, initial = {'poll': poll})
		form.fields['poll'].widget = forms.HiddenInput()
		if form.is_valid():
			messages.success(request, "Scelta Modificata")
			choice = form.save()
			return redirect('sondaggi:detail', poll.id)

		context = {
			"form": form,
		}
		return render(request, "sondaggi/poll_form.html", context)
	else:
		raise Http404


@login_required
def delete_choice_view(request, poll_id, choice_id):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		poll = Poll.objects.get(id = poll_id)
		choice = Choice.objects.get(id = choice_id)
		choice.delete()
		choices = Choice.objects.filter(poll = poll)
		if len(choices) > 0:
			return redirect("sondaggi:detail", poll.id)
		return redirect("sondaggi:index")
	else:
		raise Http404
