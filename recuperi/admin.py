from django.contrib import admin

from .models import Settimana


# Register your models here.

class SettimanaAdmin(admin.ModelAdmin):
	list_display = ('id', 'iscrizioni_aperte',)

	class Meta:
		model = Settimana


admin.site.register(Settimana, SettimanaAdmin)
