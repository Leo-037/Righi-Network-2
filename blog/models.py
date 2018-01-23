from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown
from taggit.managers import TaggableManager


def upload_location(instance, filename):
	PostModel = instance.__class__
	try:
		new_id = PostModel.objects.order_by("id").last().id + 1
	except:
		new_id = 1
	return "blog/%s/%s" % (new_id, filename)


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete = models.PROTECT)
	title = models.CharField("Titolo", max_length = 120)
	slug = models.SlugField(unique = True)
	image = models.ImageField("Immagine", upload_to = upload_location,
	                          null = True,
	                          blank = True,
	                          width_field = "width_field",
	                          height_field = "height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	content = models.TextField("Contenuto")
	draft = models.BooleanField("Bozza", default = False)
	publish = models.DateField("Data di pubblicazione", auto_now = False, auto_now_add = False,
	                           default = datetime.date.today)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

	tags = TaggableManager()

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:detail", kwargs = {"slug": self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug = slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" % (slug, qs.first().id)
		return create_slug(instance, new_slug = new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
