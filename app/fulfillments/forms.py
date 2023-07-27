from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Fulfillment


class FulfillmentForm(ModelForm):

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Create Fulfillment', css_class='btn-primary'))

    class Meta:
        model = Fulfillment
        fields = ['tracking_code', 'carrier', 'carrier_other_name']
