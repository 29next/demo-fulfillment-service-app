import django_filters

from .models import FulfillmentOrder


class FulfillmentOrderFilter(django_filters.FilterSet):

    class Meta:
        model = FulfillmentOrder
        fields = ['status']
