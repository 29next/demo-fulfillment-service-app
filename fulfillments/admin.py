from django.contrib import admin

from .models import FulfillmentOrder, FulfillmentLineItem, Fulfillment, ShippingAddress


class FulfillmentLineItemAdminInline(admin.TabularInline):
    fields = ['sku', 'qty']
    model = FulfillmentLineItem
    extra = 1


class FulfillmentOrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['store', 'location', 'shipping_address']
    list_display = ['store', 'ref_id', 'location', 'shipping_method', 'status']
    list_filter = ['status']
    inlines = [FulfillmentLineItemAdminInline]


admin.site.register(FulfillmentOrder, FulfillmentOrderAdmin)


class FulfillmentLineItemAdmin(admin.ModelAdmin):
    raw_id_fields = ['fulfillment_order']
    list_display = ['fulfillment_order', 'sku', 'qty']


admin.site.register(FulfillmentLineItem, FulfillmentLineItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'country']


admin.site.register(ShippingAddress, ShippingAddressAdmin)


class FulfillmentAdmin(admin.ModelAdmin):
    raw_id_fields = ['fulfillment_order']
    list_display = ['fulfillment_order', 'tracking_code', 'carrier']


admin.site.register(Fulfillment, FulfillmentAdmin)
