from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from righinetwork.settings import EMAIL_HOST_USER
from .models import *


# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
@login_required
def list_tutors(request):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Ripetizioni fra pari"

	tutors_utente = Tutor.objects.filter(studente = request.user.studente)

	tutors = Tutor.objects.filter(approvato = True).exclude(studente = request.user.studente)

	# query = request.GET.get("q")
	# if query:
	# 	tutors = tutors.filter(
	# 		Q(studente__nome__icontains = query) |
	# 		Q(studente__cognome__icontains = query) |
	# 		Q(materia__icontains = query)
	# 	).distinct()

	context = {"title": title,
	           "tutors": tutors,
	           "tutors_utente": tutors_utente,
	           }

	return render(request, 'tutoring/lista_tutor.html', context)


@login_required
def gestione_tutor(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		title = "Gestione tutor"

		tutors = Tutor.objects.filter(approvato = False)

		context = {"title": title,
		           "tutors": tutors,
		           }

		return render(request, 'tutoring/gestione.html', context)
	raise Http404


@login_required
def tutor_form_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	title = "Diventa tutor"
	if request.method == "POST":
		form = TutorForm(request.POST)

		if form.is_valid():
			studente = request.user.studente
			cellulare = form.cleaned_data["cellulare"]
			materia = form.cleaned_data["materia"]

			prima = form.cleaned_data["prima"]
			seconda = form.cleaned_data["seconda"]
			terza = form.cleaned_data["terza"]
			quarta = form.cleaned_data["quarta"]
			quinta = form.cleaned_data["quinta"]

			if prima == False and seconda == False and terza == False and quarta == False and quinta == False:
				prima = True
				seconda = True
				terza = True
				quarta = True
				quinta = True

			tutor = Tutor(studente = studente, cellulare = cellulare, materia = materia,
			              prima = prima,
			              seconda = seconda, terza = terza, quarta = quarta, quinta = quinta)
			tutor.save()
			messages.success(request, "Richiesta inviata. Verrà  approvata il più presto possibile",
			                 extra_tags = 'html_safe')

		return HttpResponseRedirect("/tutoring/")
	else:
		form = TutorForm()

	return render(request, 'tutoring/tutor_form.html', {'title': title, 'form': form})


@login_required
def approva_tutor(request, pk):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		tutor = Tutor.objects.get(pk = pk)
		tutor.approvato = True
		tutor.save()
		return HttpResponseRedirect("/tutoring/")
	else:
		raise Http404


@login_required
def elimina_tutor(request, pk):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		tutor = Tutor.objects.get(pk = pk)
		tutor.delete()
		return HttpResponseRedirect("/tutoring/")
	raise Http404


@login_required
def richiedi_tutor(request, pk):
	if not request.user.studente.is_attivato:
		raise Http404
	tutor = Tutor.objects.get(pk = pk)
	studente = request.user.studente
	if len(Allievo.objects.filter(tutor = tutor, studente = studente)) > 0:
		messages.success(request, "Hai già inviato una richiesta a questo tutor.", extra_tags = 'html_safe')
		return HttpResponseRedirect("/tutoring/")

	allievo = Allievo(tutor = tutor, studente = studente)
	allievo.save()
	send_mail('Tutoring',
	          """L'alunno {0} di classe {1}^{2} ha chiesto il tutoring in {3}. \nPer contattarlo, questo è il suo indirizzo email: {4}""".format(
		          studente.nome + " " + studente.cognome, str(studente.classe), studente.sezione, tutor.materia,
		          studente.user.email), EMAIL_HOST_USER,
	          [tutor.studente.user.email])

	return HttpResponseRedirect("/tutoring/")
