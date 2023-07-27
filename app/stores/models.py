from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from app.abstract_models import AbstractAddress
from .api.admin import Api


class Store(models.Model):
    ref_id = models.CharField(max_length=200, unique=True, help_text='Store Subdomain')
    api_token = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.ref_id

    def get_absolute_url(self):
        return reverse('stores:detail', args=[self.id])


class Location(AbstractAddress):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ref_id = models.IntegerField(help_text='External Reference ID', blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)

    def get_address_object(self):
        address = {
            'line1': self.line1,
            'line2': self.line2,
            'line3': self.line3,
            'line4': self.line4,
            'state': self.state,
            'postcode': self.postcode,
            'country': self.country.code
        }
        return address


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    num_in_stock = models.IntegerField(help_text='Num Available', default=0)

    class Meta:
        unique_together = [['store', 'location', 'sku']]

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('stores:product-update', args=[self.id])


@receiver(post_save, sender=Location)
def create_location(sender, instance, created, **kwargs):
    if created:
        result = Api(
            store_id=instance.store.ref_id,
            access_token=instance.store.api_token
        ).create_location(
            name=instance.name,
            address=instance.get_address_object()
        )
        instance.ref_id = result.json().get('id')
        instance.save()
    return instance
