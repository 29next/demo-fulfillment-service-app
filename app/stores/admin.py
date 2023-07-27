from django.contrib import admin
from .models import Store, Location, Product


class StoreLocationInline(admin.TabularInline):
    fields = ['name', 'sku', 'num_in_stock', 'store', 'location']
    model = Product
    extra = 1


class StoreProductInline(admin.TabularInline):
    fields = ['name', 'line1', 'state', 'postcode', 'country']
    model = Location
    extra = 1


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['store', 'name']
    list_display = ['store', 'name', 'line1', 'state', 'postcode', 'country']


admin.site.register(Location, LocationAdmin)


class StoreAdmin(admin.ModelAdmin):
    search_fields = ['ref_id']
    list_filter = ['status']
    list_display = ['ref_id', 'status']
    inlines = [StoreLocationInline, StoreProductInline]


admin.site.register(Store, StoreAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['store', 'name', 'location', 'sku']
    list_display = ['name', 'sku', 'num_in_stock', 'store', 'location']


admin.site.register(Product, ProductAdmin)
