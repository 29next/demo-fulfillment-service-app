from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


from users import views as user_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('stores/', include('stores.urls', namespace='stores')),
    path('fulfillments/', include('fulfillments.urls', namespace='fulfillments')),
    path('', user_views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
