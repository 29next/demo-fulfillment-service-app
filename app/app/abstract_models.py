from django.db import models
from django_countries.fields import CountryField


class AbstractAddress(models.Model):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    line3 = models.CharField(max_length=255, blank=True)
    line4 = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255)
    postcode = models.CharField(max_length=64)
    country = CountryField()

    class Meta:
        abstract = True


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
