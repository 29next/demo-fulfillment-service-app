import os
import json
import urllib

from django.core.files import File
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseGone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.generic import CreateView, ListView, View
from django_tables2 import SingleTableMixin, MultiTableMixin

from stores.api.admin import Api
from stores.models import Store, Product, Location
from .models import FulfillmentOrder, FulfillmentLineItem, ShippingAddress
from .forms import FulfillmentForm
from . import filters as filters
from . import tables as tables


@method_decorator(csrf_exempt, name='dispatch')
class FulfillmentOrderNotificationReceiver(View):

    def products_available(self, store, location, lines):
        # check all products are in stock at location
        try:
            for each in lines:
                Product.objects.get(store=store, location=location, sku=each['sku'], num_in_stock__gt=0)
            valid = True
        except:
            valid = False
        return valid

    def post(self, request):
        request_data = json.loads(self.request.body)
        request_type = request_data.get('type', {})
        store_ref_id = request.headers.get('X-29Next-Store', None)
        store = Store.objects.get(ref_id=store_ref_id)

        if store and request_type == 'fulfillment_requested':

            open_fulfillment_requests = Api(
                store.ref_id, store.api_token).get_requested_fulfillment_orders()

            for each in open_fulfillment_requests.json().get('results'):
                location = Location.objects.get(ref_id=each['assigned_location']['id'])

                if self.products_available(store, location, each['line_items']):
                    shipping_address = ShippingAddress.objects.create(
                        first_name=each['shipping_address']['first_name'],
                        last_name=each['shipping_address']['last_name'],
                        line1=each['shipping_address']['line1'],
                        line2=each['shipping_address']['line2'],
                        line3=each['shipping_address']['line3'],
                        line4=each['shipping_address']['line4'],
                        state=each['shipping_address']['state'],
                        postcode=each['shipping_address']['postcode'],
                        country=each['shipping_address']['country'],
                        phone_number=each['shipping_address']['phone_number'],
                    )
                    fulfillment_order = FulfillmentOrder.objects.create(
                        store=store,
                        location=location,
                        ref_id=each['id'],
                        order_number=each['order_number'],
                        shipping_method=each['shipping_method']['code'],
                        shipping_address=shipping_address
                    )
                    for line in each['line_items']:
                        product = Product.objects.get(store=store, location=location, sku=line['sku'])
                        FulfillmentLineItem.objects.create(
                            fulfillment_order=fulfillment_order,
                            product=product,
                            sku=line['sku'],
                            qty=line['quantity']
                        )
                        # update product image
                        product_image_url = line.get('product_image', None)
                        if not product.image and product_image_url:
                            result = urllib.request.urlretrieve(product_image_url)
                            product.image.save(
                                os.path.basename(product_image_url),
                                File(open(result[0], 'rb'))
                            )
                        # update product name
                        product_name = line.get('product_title', None)
                        print(product_name)
                        print(product.name)
                        if product_name and product.name != product_name:
                            print(product_name)
                            product.name = product_name
                            product.save()

                    # Accept the fulfillment request
                    message = 'Fulfillment will be processed shortly.'
                    Api(store.ref_id, store.api_token).accept_fulfillment_request(each['id'], message)
                else:
                    # Reject the fulfillment request
                    message = 'Products not available at location.'
                    Api(store.ref_id, store.api_token).reject_fulfillment_request(each['id'], message)

        elif store and request_type == 'cancellation_requested':

            open_cancellation_requests = Api(
                store.ref_id, store.api_token).get_cancellation_requested_fulfillment_orders()

            for each in open_cancellation_requests.json().get('results'):
                fulfillment_order = FulfillmentOrder.objects.get(store=store, ref_id=each['id'])
                if fulfillment_order.status == 'open':
                    # Accept the cancellation
                    message = 'Fulfillment canceled.'
                    Api(store.ref_id, store.api_token).accept_cancellation_request(each['id'], message)
                    fulfillment_order.status = 'canceled'
                    fulfillment_order.save()

                elif fulfillment_order.status == 'shipped':
                    # Reject the cancellation
                    message = 'Already shipped.'
                    Api(store.ref_id, store.api_token).reject_cancellation_request(each['id'], message)
        else:
            HttpResponseGone('gone')

        return HttpResponse('success')


class FulfillmentOrderListView(LoginRequiredMixin, SingleTableMixin, ListView):
    template_name = 'fulfillments/fo-list.html'
    filter_class = filters.FulfillmentOrderFilter
    table_class = tables.FulfillmentOrderListTable
    model = FulfillmentOrder

    def get_filters(self):
        return self.filter_class(self.request.GET, queryset=self.get_queryset())

    def get_queryset(self):
        qs = self.queryset
        return self.filter_class(self.request.GET, queryset=qs).qs


class FulfillmentOrderDetailView(LoginRequiredMixin, MultiTableMixin, CreateView):
    template_name = 'fulfillments/fo-detail.html'
    form_class = FulfillmentForm
    tables = [
        tables.FulfillmentLineItemsTable,
        tables.FulfillmentsTable
    ]

    def get_queryset(self):
        return FulfillmentOrder.objects.get(pk=self.kwargs.get('pk'))

    def get_tables_data(self):
        return [
            FulfillmentLineItem.objects.filter(fulfillment_order__id=self.kwargs.get('pk')),
            self.get_queryset().fulfillment_set.all()
        ]

    def form_valid(self, form, **kwargs):
        fulfillment_order = self.get_queryset(**kwargs)
        form.instance.fulfillment_order = fulfillment_order
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_queryset()
        return context

    def get_success_url(self):
        return reverse('fulfillments:fo-detail', args=[self.kwargs.get('pk')])
