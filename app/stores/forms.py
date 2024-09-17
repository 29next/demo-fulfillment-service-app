from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product, Location


class StoreProductCreateForm(ModelForm):

    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.fields['location'].queryset = Location.objects.filter(store=store)

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Create Product', css_class='btn-primary'))

    class Meta:
        model = Product
        fields = ['name', 'sku', 'location', 'num_in_stock']


class StoreProductUpdateForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update Product', css_class='btn-primary'))

    class Meta:
        model = Product
        fields = ['name', 'sku', 'num_in_stock']


class StoreLocationCreateForm(ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Create Location', css_class='btn-primary'))

    class Meta:
        model = Location
        fields = [
            'name', 'line1', 'line2', 'line3', 'line4', 'state', 'postcode', 'country'
        ]
