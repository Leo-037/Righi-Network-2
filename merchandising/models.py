from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


def upload_location(instance, filename):
	ProductModel = instance.__class__
	try:
		new_id = ProductModel.objects.order_by("id").last().id + 1
	except:
		new_id = 1
	return "merchandising/%s/%s" % (new_id, filename)


class Prodotto(models.Model):
	nome = models.CharField(max_length = 150)
	descrizione = models.TextField(null = True, blank = True)
	foto = models.ImageField(upload_to = upload_location, null = True, blank = True)
	costo = models.DecimalField(max_digits = 6, decimal_places = 2, null = True, blank = True)

	tags = TaggableManager()

	def get_absolute_url(self):
		return reverse('merchandising:prodotto', kwargs = {'pk': self.pk})
