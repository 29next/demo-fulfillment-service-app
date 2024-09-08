from django.views.generic.base import RedirectView
from django.urls import reverse


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('fulfillments:fo-list')
