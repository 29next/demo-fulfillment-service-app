import django_tables2 as tables

from .models import Store, Product, Location


class StoresListTable(tables.Table):
    id = tables.Column(linkify=True)
    ref_id = tables.Column(linkify=True)

    class Meta:
        model = Store
        fields = ['id', 'ref_id', 'status']


class StoreProductsTable(tables.Table):
    name = tables.Column(linkify=True)

    class Meta:
        model = Product
        fields = ['name', 'sku', 'num_in_stock', 'location']


class StoreLocationsTable(tables.Table):
    class Meta:
        model = Location
        fields = ['name', 'line1', 'country']
