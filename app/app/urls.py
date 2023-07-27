from django.contrib import admin
from django.urls import include, path

from users import views as user_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('stores/', include('stores.urls', namespace='stores')),
    path('fulfillments/', include('fulfillments.urls', namespace='fulfillments')),
    path('', user_views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]
