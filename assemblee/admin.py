from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from .forms import TurnoAdminForm, GruppoAdminForm, IscrittoAdminForm
from .models import Assemblea, Turno, Gruppo, Iscritto


class TurnoInline(admin.TabularInline):
	model = Turno
	form = TurnoAdminForm
	can_delete = False
	verbose_name_plural = 'Turni'
	extra = 0


class GruppoInline(admin.StackedInline):
	model = Gruppo
	form = GruppoAdminForm
	can_delete = False
	verbose_name_plural = 'Gruppi'
	extra = 0


class IscrittoInline(admin.StackedInline):
	model = Iscritto
	form = IscrittoAdminForm
	can_delete = False
	verbose_name_plural = 'Iscritti'


class AssembleaModelAdmin(admin.ModelAdmin):
	list_display = ["data", "sede", "mostra", "iscrizioni_aperte", "numero_turni", "edit_turni"]
	list_display_links = ["data"]
	list_filter = ["data", "sede"]
	search_fields = ["data"]

	inlines = [
		TurnoInline,
	]

	def numero_turni(self, obj):
		turni = Turno.objects.filter(assemblea = obj.id)
		parola = "Turni"
		if len(turni) == 0:
			return None
		elif len(turni) == 1:
			parola = "Turno"
		return str(len(turni)) + " " + parola

	numero_turni.short_description = 'numero turni'
	numero_turni.admin_order_field = 'id'
	numero_turni.allow_tags = True
	numero_turni.empty_value_display = 'Nessun turno'

	def edit_turni(self, obj, **kwargs):
		return format_html(
			'<a href = "/admin/assemblee/turno/?assemblea__id__exact=%s">Edit Turni</a>' % (
				obj.id))

	class Meta:
		model = Assemblea
		verbose_name_plural = "Assemblee"


class TurnoModelAdmin(admin.ModelAdmin):
	list_display = ["inizio", "fine", "numero_gruppi", "desc_assemblea", "edit_gruppi"]
	list_filter = ["inizio"]
	list_search = ["fine"]

	inlines = [
		GruppoInline,
	]

	def numero_gruppi(self, obj):
		gruppi = Gruppo.objects.filter(turno = obj.id)
		parola = "Gruppi"
		if len(gruppi) == 0:
			return None
		elif len(gruppi) == 1:
			parola = "Gruppo"
		return str(len(gruppi)) + " " + parola

	numero_gruppi.short_description = 'Numero gruppi'
	numero_gruppi.admin_order_field = 'id'
	numero_gruppi.allow_tags = True
	numero_gruppi.empty_value_display = 'Nessun gruppo'

	def desc_assemblea(self, obj):
		return obj.assemblea.data_assemblea

	desc_assemblea.short_description = "Assemblea"
	desc_assemblea.admin_order_field = "id"
	desc_assemblea.allow_tags = True

	def edit_gruppi(self, obj, **kwargs):
		return format_html(
			'<a href = "/admin/assemblee/gruppo/?turno__id__exact=%s">Edit Gruppi</a>' % (
				obj.id))

	form = TurnoAdminForm

	class Meta:
		model = Turno
		verbose_name_plural = "Turni"


class GruppoModelAdmin(admin.ModelAdmin):
	list_display = ["titolo", "aula", "descrizione", "host", "mostra_iscritti", "desc_turno", "desc_assemblea"]
	list_display_links = ["titolo"]
	list_filter = ["titolo", "aula", "host"]
	list_search = ["titolo", "aula", "host"]

	inlines = [
		IscrittoInline,
	]

	def mostra_iscritti(self, obj):
		return "{0}/{1}".format(obj.iscritti, obj.iscritti_massimi)

	mostra_iscritti.short_description = "Iscritti"

	def desc_turno(self, obj):
		return format_html(
			'<a href = "/admin/assemblee/turno/%s/change">Dalle %s alle %s</a>' % (
				obj.turno.id, obj.turno.ora, obj.turno.orario_fine))

	desc_turno.short_description = "Turno"
	desc_turno.admin_order_field = "id"
	desc_turno.allow_tags = True

	def desc_assemblea(self, obj):
		if settings.DEBUG:
			return format_html(
				'<a href = "http://127.0.0.1:8000/admin/assemblee/assemblea/%s/change">%s</a>' % (
					obj.turno.assemblea.id, obj.turno.assemblea.data_assemblea))

		else:
			return format_html(
				'<a href = "http://www.righi-network.it/admin/assemblee/assemblea/%s/change">%s</a>' % (
					obj.turno.assemblea.id, obj.turno.assemblea.data_assemblea))

	desc_assemblea.short_description = "Assemblea"
	desc_assemblea.admin_order_field = "id"
	desc_assemblea.allow_tags = True

	form = GruppoAdminForm

	class Meta:
		model = Gruppo
		verbose_name_plural = "Gruppi"


class IscrittoModelAdmin(admin.ModelAdmin):
	list_display = ["mostra_studente", "mostra_gruppo", "turno", "assemblea"]

	def mostra_studente(self, obj):
		return str(obj.studente.user.username)

	def mostra_gruppo(self, obj):
		return str(obj.gruppo.titolo)

	def turno(self, obj):
		return "dalle {} alle {}".format(obj.gruppo.turno.ora, obj.gruppo.turno.orario_fine)

	def assemblea(self, obj):
		return str(obj.gruppo.turno.assemblea.data_assemblea)

	form = IscrittoAdminForm

	class Meta:
		model = Iscritto
		verbose_name_plural = "Iscritti"


admin.site.register(Assemblea, AssembleaModelAdmin)
admin.site.register(Turno, TurnoModelAdmin)
admin.site.register(Gruppo, GruppoModelAdmin)
admin.site.register(Iscritto, IscrittoModelAdmin)
