from django.urls import path

from . import views


app_name = 'fulfillments'
urlpatterns = [
    path(
        'fulfillment-order-notification/',
        views.FulfillmentOrderNotificationReceiver.as_view(),
        name='fo-notification-receiver'
    ),
    path('orders/', views.FulfillmentOrderListView.as_view(), name='fo-list'),
    path('orders/<pk>/', views.FulfillmentOrderDetailView.as_view(), name='fo-detail'),
]
