from django.contrib.auth.models import User
from django.db import models


# Custom model fields

class UpperCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop('uppercase', False)
        super(UpperCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(UpperCharField, self).get_prep_value(value)
        if self.is_uppercase:
            return value.upper()

        return value


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


# Models


COLORI = (('red', 'Rosso'),
          ('orange', 'Arancione'),
          ('yellow', 'Giallo'),
          ('olive', 'Verde Chiaro'),
          ('green', 'Verde'),
          ('teal', 'Azzurro'),
          ('blue', 'Blu'),
          ('violet', 'Viola'),
          ('purple', 'Porpora'),
          ('pink', 'Rosa'),
          ('brown', 'Marrone'),
          ('grey', 'Grigio'),
          ('black', 'Nero'))

class Studente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    classe = IntegerRangeField(min_value=1, max_value=5)
    sezione = UpperCharField(max_length=1, uppercase=True)

    colore = models.CharField(max_length = 6, choices = COLORI, default = 'green')

    is_rapclasse = models.BooleanField(default=False)
    is_rapistituto = models.BooleanField(default=False)

    is_attivato = models.BooleanField(default=False)
    otpassword = models.CharField(max_length=8, blank=True)


class DummyUser(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    otpassword = models.CharField(max_length=8)
    studente = models.OneToOneField(Studente, on_delete=models.CASCADE)


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    password = models.CharField(max_length=8, blank=True)
