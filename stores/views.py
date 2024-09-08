import json
import requests

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, RedirectView, UpdateView, View
from django_tables2 import SingleTableMixin, MultiTableMixin

from .api.admin import Api
from .api.webhooks import webhook_payload_validator
from .models import Store, Location, Product
from . import forms as forms
from . import tables as tables


class StoreAuthHandler(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        network_domain = self.request.GET.get('store', None)
        token = self.request.GET.get('token', None)
        store_id = network_domain.split('.', 1)[0]
        store = Store.objects.filter(ref_id=store_id, status=True)

        # Initial install flow doesnt have a token parameter
        if network_domain and not token:
            permission_setup_url = 'https://{network_domain}/oauth2/authorize/?response_type=code&'
            permission_setup_url += 'client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}'
            redirect_url = permission_setup_url.format(
                network_domain=network_domain,
                client_id=settings.CLIENT_ID,
                redirect_uri=settings.APP_DOMAIN + reverse('stores:setup'),
                scopes=settings.SCOPES
            )
            return redirect_url

        # If token is present, the app is installed on a store
        elif token:
            return reverse('stores:detail', args=[store.first().id])
        else:
            return '/'


class StoreAuthSetup(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        network_domain = self.request.GET.get('store', None)
        store_id = network_domain.split('.', 1)[0]
        auth_code = self.request.GET.get('code', None)

        # Request a new api access token
        url = 'https://{}/oauth2/token/'.format(network_domain)
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'redirect_uri': settings.APP_DOMAIN + reverse('stores:setup'),
            'code': auth_code
        }
        response = requests.post(url, data=data)

        # Save api access token with store for future use
        store, created = Store.objects.get_or_create(ref_id=store_id)
        store.api_token = response.json().get('access_token', '')
        store.status = True
        store.save()

        # Setup webhooks to listen to new orders and app.uninstalled event
        Api(store_id, store.api_token).create_webhook(
            settings.WEBHOOK_EVENTS, settings.WEBHOOK_NAME,
            settings.APP_DOMAIN + reverse('stores:webhook_processor')
        )
        # Redirect to store settings once install flow is complete complete
        return reverse('stores:detail', args=[store.id])


class StoresListView(LoginRequiredMixin, SingleTableMixin, ListView):
    template_name = 'stores/list.html'
    table_class = tables.StoresListTable
    model = Store


class StoresDetailView(LoginRequiredMixin, MultiTableMixin, DetailView):
    template_name = 'stores/detail.html'
    model = Store
    tables = [
        tables.StoreProductsTable,
        tables.StoreLocationsTable
    ]

    def get_tables_data(self):
        return [
            Product.objects.filter(store=self.get_object()),
            Location.objects.filter(store=self.get_object())
        ]


class StoreProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'stores/product-create.html'
    form_class = forms.StoreProductCreateForm

    def get_queryset(self):
        return Store.objects.get(pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['store'] = self.get_queryset()
        return kwargs

    def form_valid(self, form, **kwargs):
        form.instance.store = self.get_queryset(**kwargs)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stores:detail', args=[self.kwargs.get('pk')])


class StoreLocationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'stores/location-create.html'
    form_class = forms.StoreLocationCreateForm

    def get_queryset(self):
        return Store.objects.get(pk=self.kwargs.get('pk'))

    def form_valid(self, form, **kwargs):
        form.instance.store = self.get_queryset(**kwargs)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('stores:detail', args=[self.kwargs.get('pk')])


class StoreProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'stores/product-update.html'
    form_class = forms.StoreProductUpdateForm

    def get_object(self):
        return Product.objects.get(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('stores:detail', args=[self.kwargs.get('pk')])


@method_decorator(csrf_exempt, name='dispatch')
class StoreWebhookProcessor(View):

    def post(self, request):
        webhook_data = json.loads(self.request.body)
        event_type = webhook_data.get('event_type', None)
        event_source_store = webhook_data.get('webhook', {}).get('store', None)
        store = Store.objects.get(ref_id=event_source_store)

        # Validate webhook data
        valid = webhook_payload_validator(
            json.dumps(webhook_data), self.request.headers.get('X-29Next-Signature', None))

        if valid and event_source_store and store:

            # Deactivate the store if app is uninstalled
            if event_type == 'app.uninstalled':
                store.status = False
                store.save()

        return HttpResponse('success')
