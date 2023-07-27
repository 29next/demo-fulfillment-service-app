from django.urls import path

from . import views


app_name = 'stores'
urlpatterns = [
    path('auth/login/', views.StoreAuthHandler.as_view(), name='login'),
    path('auth/setup/', views.StoreAuthSetup.as_view(), name='setup'),
    path('webhooks/', views.StoreWebhookProcessor.as_view(), name='webhook_processor'),
    path('', views.StoresListView.as_view(), name='list'),
    path('<pk>/', views.StoresDetailView.as_view(), name='detail'),
    path('<pk>/products/create/', views.StoreProductCreateView.as_view(), name='product-create'),
    path('products/<pk>/', views.StoreProductUpdateView.as_view(), name='product-update'),
    path('<pk>/locations/create/', views.StoreLocationCreateView.as_view(), name='location-create'),

]
