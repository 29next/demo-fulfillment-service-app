from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from app.abstract_models import AbstractAddress, Timestampable

from stores.models import Store, Location, Product
from stores.api.admin import Api


FO_STATUSES = [
    ('open', 'Open'),
    ('shipped', 'Shipped'),
    ('canceled', 'Canceled'),
]

CARRIERS = [
    ('dhl_ecommerce', 'DHL Ecommerce'),
    ('fedex', 'FedEx'),
    ('ups', 'UPS'),
    ('usps', 'USPS'),
    ('other', 'Other'),
]


class ShippingAddress(AbstractAddress):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '{} {} - {}, {}, {} {}'.format(
            self.first_name, self.last_name, self.line1, self.line4, self.postcode, self.country
        )


class FulfillmentOrder(Timestampable, models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    ref_id = models.IntegerField()
    order_number = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=FO_STATUSES, default='open')
    shipping_method = models.CharField(max_length=255)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} - {}'.format(self.store, self.ref_id)

    def get_absolute_url(self):
        return reverse('fulfillments:fo-detail', args=[self.id])


class FulfillmentLineItem(models.Model):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} - {} - {}'.format(self.fulfillment_order, self.sku, self.qty)


class Fulfillment(models.Model):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    tracking_code = models.CharField(max_length=255)
    carrier = models.CharField(max_length=50, choices=CARRIERS, default='dhl_ecommerce')
    carrier_other_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.fulfillment_order, self.tracking_code, self.carrier)


@receiver(post_save, sender=Fulfillment)
def create_fulfillment(sender, instance, **kwargs):
    Api(
        store_id=instance.fulfillment_order.store.ref_id,
        access_token=instance.fulfillment_order.store.api_token
    ).create_fulfillment(
        fulfillment_order_id=instance.fulfillment_order.ref_id,
        tracking_code=instance.tracking_code,
        carrier=instance.carrier,
        carrier_other_name=instance.carrier_other_name
    )
    instance.fulfillment_order.status = 'shipped'
    instance.fulfillment_order.save()
