from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .models import *


@login_required
def create_gruppo_view(request):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		if request.method == "GET":
			form = GruppoForm()
			return render(request, 'recuperi/form.html', {'title': "Aggiungi Gruppo", 'form': form})
		elif request.method == "POST":
			form = GruppoForm(request.POST)
			form.save()

			return redirect("recuperi:main")
	raise Http404


@login_required
def gruppo_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	settimane = Settimana.objects.all()
	iscrizioni_aperte = settimane[0].iscrizioni_aperte if len(settimane) > 0 else False

	gruppo = Gruppo.objects.get(id = id_gruppo)

	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__user__last_name")

	gruppo_lunedi = False
	gruppo_martedi = False
	gruppo_mercoledi = False
	gruppo_giovedi = False
	gruppo_venerdi = False

	for gia_iscritto in Gruppo.objects.all():
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__lunedi = True):
			gruppo_lunedi = gia_iscritto
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__martedi = True):
			gruppo_martedi = gia_iscritto
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__mercoledi = True):
			gruppo_mercoledi = gia_iscritto
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__giovedi = True):
			gruppo_giovedi = gia_iscritto
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__venerdi = True):
			gruppo_venerdi = gia_iscritto

	gruppi_iscritto = []
	gruppi_iscritto.append(gruppo_lunedi)
	gruppi_iscritto.append(gruppo_martedi)
	gruppi_iscritto.append(gruppo_mercoledi)
	gruppi_iscritto.append(gruppo_giovedi)
	gruppi_iscritto.append(gruppo_venerdi)

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
		'gruppo_lunedi': gruppo_lunedi,
		'gruppo_martedi': gruppo_martedi, 'gruppo_mercoledi': gruppo_mercoledi,
		'gruppo_giovedi': gruppo_giovedi, 'gruppo_venerdi': gruppo_venerdi,
		'gruppi_iscritto': gruppi_iscritto, 'iscrizioni_aperte': iscrizioni_aperte,
		'iscritti': iscritti
	}

	return render(request, 'recuperi/gruppo.html', context)


@login_required
def update_gruppo_view(request, id_gruppo):
	if not request.user.studente.is_rapistituto and not request.user.is_superuser:
		raise Http404
	gruppo = get_object_or_404(Gruppo, id = id_gruppo)
	form = GruppoForm(request.POST or None, request.FILES or None, instance = gruppo)
	if form.is_valid():
		gruppo = form.save(commit = False)
		gruppo.save()
		messages.success(request, "Gruppo salvato", extra_tags = 'html_safe')
		return redirect(
			"recuperi:main")
	context = {
		"title": "Modifica gruppo",
		"gruppo": gruppo,
		"form": form,
	}
	return render(request, "recuperi/form.html", context)


@login_required
def delete_gruppo_view(request, id_gruppo):
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		gruppo.delete()
		messages.success(request, "Cancellato", extra_tags = 'html_safe')
		return redirect("recuperi:main")
	raise Http404


@login_required
def recuperi_view(request):
	if not request.user.studente.is_attivato:
		raise Http404

	settimane = Settimana.objects.all()
	iscrizioni_aperte = settimane[0].iscrizioni_aperte if len(settimane) > 0 else False

	studente = Studente.objects.get(user = request.user)

	gruppi = Gruppo.objects.all()
	if not (request.user.studente.is_rapistituto or request.user.is_superuser):
		if studente.classe == 1:
			gruppi = gruppi.exclude(prima = False)
		if studente.classe == 2:
			gruppi = gruppi.exclude(seconda = False)
		if studente.classe == 3:
			gruppi = gruppi.exclude(terza = False)
		if studente.classe == 4:
			gruppi = gruppi.exclude(quarta = False)
		if studente.classe == 5:
			gruppi = gruppi.exclude(quinta = False)

	gruppi = gruppi.order_by('venerdi', 'giovedi', 'mercoledi', 'martedi', 'lunedi')

	gruppo_lunedi = False
	gruppo_martedi = False
	gruppo_mercoledi = False
	gruppo_giovedi = False
	gruppo_venerdi = False

	for gruppo in gruppi:
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo,
		                           gruppo__lunedi = True):
			gruppo_lunedi = gruppo
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo,
		                           gruppo__martedi = True):
			gruppo_martedi = gruppo
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo,
		                           gruppo__mercoledi = True):
			gruppo_mercoledi = gruppo
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo,
		                           gruppo__giovedi = True):
			gruppo_giovedi = gruppo
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gruppo,
		                           gruppo__venerdi = True):
			gruppo_venerdi = gruppo

	gruppi_iscritto = []
	gruppi_iscritto.append(gruppo_lunedi)
	gruppi_iscritto.append(gruppo_martedi)
	gruppi_iscritto.append(gruppo_mercoledi)
	gruppi_iscritto.append(gruppo_giovedi)
	gruppi_iscritto.append(gruppo_venerdi)

	return render(request, 'recuperi/settimana.html',
	              context = {'title': 'Settimana dei recuperi', 'gruppi': gruppi, 'gruppo_lunedi': gruppo_lunedi,
	                         'gruppo_martedi': gruppo_martedi, 'gruppo_mercoledi': gruppo_mercoledi,
	                         'gruppo_giovedi': gruppo_giovedi, 'gruppo_venerdi': gruppo_venerdi,
	                         'iscrizioni_aperte': iscrizioni_aperte,
	                         'gruppi_iscritto': gruppi_iscritto, })


@login_required
def apri_iscrizioni_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		settimana = Settimana.objects.all()[0]
		settimana.iscrizioni_aperte = True
		settimana.save()
		return redirect("recuperi:main")
	raise Http404


@login_required
def chiudi_iscrizioni_view(request):
	if not request.user.studente.is_attivato:
		raise Http404
	if request.user.studente.is_rapistituto or request.user.is_superuser:
		settimana = Settimana.objects.all()[0]
		settimana.iscrizioni_aperte = False
		settimana.save()
		return redirect("recuperi:main")
	raise Http404


@login_required
def iscrizione_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	settimane = Settimana.objects.all()
	iscrizioni_aperte = settimane[0].iscrizioni_aperte if len(settimane) > 0 else False

	gruppo = Gruppo.objects.get(id = id_gruppo)
	classi_gruppo = []
	if gruppo.prima:
		classi_gruppo.append(1)
	if gruppo.seconda:
		classi_gruppo.append(2)
	if gruppo.terza:
		classi_gruppo.append(3)
	if gruppo.quarta:
		classi_gruppo.append(4)
	if gruppo.quinta:
		classi_gruppo.append(5)

	studente = Studente.objects.get(user = request.user)

	for gia_iscritto in Gruppo.objects.all():
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__lunedi = True) and gruppo.lunedi:
			raise Http404
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__martedi = True) and gruppo.martedi:
			raise Http404
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__mercoledi = True) and gruppo.mercoledi:
			raise Http404
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__giovedi = True) and gruppo.giovedi:
			raise Http404
		if Iscritto.objects.filter(studente = request.user.studente, gruppo = gia_iscritto,
		                           gruppo__venerdi = True) and gruppo.venerdi:
			raise Http404

	if studente.classe in classi_gruppo:
		if not gruppo.iscritti == gruppo.iscritti_massimi and iscrizioni_aperte:
			iscritto = Iscritto(studente = request.user.studente, gruppo = gruppo)
			gruppo.iscritti += 1
			iscritto.save()
			gruppo.save()

			next = request.GET.get("next")
			if next:
				return redirect(next)
			return redirect("recuperi:main")
	raise Http404


@login_required
def disiscrizione_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404

	settimane = Settimana.objects.all()
	iscrizioni_aperte = settimane[0].iscrizioni_aperte if len(settimane) > 0 else False
	if iscrizioni_aperte:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		iscritto = Iscritto.objects.get(studente = request.user.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		next = request.GET.get("next")
		if next:
			return redirect(next)
		return redirect("recuperi:main")
	raise Http404


@login_required
def disiscrivi_view(request, id_gruppo, id_utente):
	if not request.user.studente.is_attivato:
		raise Http404

	if request.user.studente.is_rapistituto or request.user.is_superuser:
		gruppo = Gruppo.objects.get(id = id_gruppo)
		utente = User.objects.get(id = id_utente)
		iscritto = Iscritto.objects.get(studente = utente.studente, gruppo = gruppo)
		gruppo.iscritti -= 1
		iscritto.delete()
		gruppo.save()

		return redirect("recuperi:main")
	else:
		raise Http404


@login_required
def pdf_iscritti_view(request, id_gruppo):
	if not request.user.studente.is_attivato:
		raise Http404
	gruppo = Gruppo.objects.get(pk = id_gruppo)
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'attachment; filename="' + gruppo.titolo + '".pdf"'

	buffer = BytesIO()

	doc = SimpleDocTemplate(buffer, rightMargin = 35,
	                        leftMargin = 35, topMargin = 35, bottomMargin = 18)
	doc.pagesize = portrait(A4)
	styles = getSampleStyleSheet()

	# TITOLO

	styles.add(ParagraphStyle(name = 'Custom', fontSize = 19, alignment = 1, wordWrap = 'CJK', leading = 25))

	giorni = []
	if gruppo.lunedi:
		giorni.append("Lunedì")
	if gruppo.martedi:
		giorni.append("Martedì")
	if gruppo.mercoledi:
		giorni.append("Mercoledì")
	if gruppo.giovedi:
		giorni.append("Giovedì")
	if gruppo.venerdi:
		giorni.append("Venerdì")

	str_giorni = ""
	for i in giorni:
		str_giorni += i + "-"
	str_giorni = str_giorni[:-1]

	titolo = Paragraph(gruppo.titolo + " di " + str_giorni + " in " + gruppo.aula,
	                   styles['Custom'])

	# TABELLA

	elements = []

	iscritti = Iscritto.objects.filter(gruppo = gruppo).order_by("studente__classe", "studente__sezione",
	                                                             "studente__user__last_name")
	data = [
		["<strong>#</strong>", "<strong>Cognome</strong>", "<strong>Nome</strong>", "<strong>Classe</strong>",
		 "<strong>Firma</strong>"]
	]

	stile_tablehead = styles["Normal"]
	stile_tablehead.alignment = 1
	data = [[Paragraph(cell, stile_tablehead) for cell in row] for row in data]

	s = getSampleStyleSheet()
	s = s["Normal"]
	s.textColor = colors.white

	i = 1
	for iscritto in iscritti:
		row = [str(i), iscritto.studente.user.last_name, iscritto.studente.user.first_name,
		       str(iscritto.studente.classe) + "^" + iscritto.studente.sezione, Paragraph("_" * 40, s)]
		data.append(row)
		i += 1

	style = TableStyle([
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black),
		('TEXTCOLOR', (4, 1), (4, -1), colors.white)
	])

	#
	t = Table(data, colWidths = "*")
	t.setStyle(style)

	elements.append(titolo)
	elements.append(Spacer(1, 0.5 * cm))
	elements.append(t)
	doc.build(elements)

	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)

	return response
