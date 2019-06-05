from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from hijack_admin.admin import HijackUserAdminMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Studente, DummyUser


class StudenteInline(admin.StackedInline):
	model = Studente
	can_delete = False
	verbose_name_plural = 'Studenti'


class UserResource(resources.ModelResource):
	class Meta:
		model = User
	# skip_unchanged = True
	# report_skipped = True

class StudenteResource(resources.ModelResource):
	class Meta:
		model = Studente
	# skip_unchanged = True
	# report_skipped = True

class DummyUserModelAdmin(admin.ModelAdmin):
	list_display = ["username", "first_name", "last_name", "otpassword"]
	list_filter = ["username", "first_name", "last_name", ]
	search_fields = ["username", "first_name", "last_name", ]
	class Meta:
		model = DummyUser


class StudenteModelAdmin(ImportExportModelAdmin):
	resource_class = StudenteResource

	list_display = ["user", "email", "nome", "cognome", "classe", "sezione", "rappr_classe", "rappr_istituto"]
	list_display_links = ["user"]
	list_filter = ["classe", "sezione", "is_rapclasse", "is_rapistituto"]
	search_fields = ["classe", "sezione", "is_rapclasse", "is_rapistituto"]

	def user(self, obj):
		if obj.user:
			return obj.user
		else:
			return "Studente non attivo"

	def nome(self, obj):
		if obj.user:
			return obj.user.first_name
		else:
			return "/"

	def cognome(self, obj):
		if obj.user:
			return obj.user.last_name
		else:
			return "/"

	def rappr_classe(self, obj):
		return obj.is_rapclasse

	rappr_classe.short_description = "Rappresentante di classe"
	rappr_classe.boolean = True

	def rappr_istituto(self, obj):
		return obj.is_rapistituto

	rappr_istituto.short_description = "Rappresentante d'istituto"
	rappr_istituto.boolean = True

	def email(self, obj):
		if obj.user:
			return obj.user.email
		else:
			return "/"

	class Meta:
		model = Studente
		verbose_name = "Studente"
		verbose_name_plural = "Studenti"


class UserAdmin(ImportExportModelAdmin, BaseUserAdmin, HijackUserAdminMixin):
	resource_class = UserResource

	list_display = ["username", "email", "is_staff", "hijack_field"]
	inlines = (StudenteInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Studente, StudenteModelAdmin)
