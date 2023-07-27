import django_tables2 as tables
from django_tables2.utils import A

from .models import FulfillmentOrder, FulfillmentLineItem, Fulfillment


class FulfillmentOrderListTable(tables.Table):
    id = tables.LinkColumn('fulfillments:fo-detail', args=[A('pk')])
    order_number = tables.Column(linkify=True)
    status = tables.TemplateColumn(template_name='tables/fulfillment_status_column.html')
    detail = tables.LinkColumn(
        'fulfillments:fo-detail', args=[A('pk')],
        attrs={'a': {'class': 'btn btn-sm btn-white'}}, text='View'
    )

    class Meta:
        model = FulfillmentOrder
        empty_text = 'No Fulfillment orders found.'
        fields = [
            'id', 'store', 'order_number', 'created_at', 'shipping_method', 'status', 'detail'
        ]


class FulfillmentLineItemsTable(tables.Table):

    class Meta:
        model = FulfillmentLineItem
        fields = ['product', 'sku', 'qty']


class FulfillmentsTable(tables.Table):

    class Meta:
        model = Fulfillment
        fields = ['carrier', 'tracking_code']
