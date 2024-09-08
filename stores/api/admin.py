import requests

from django.conf import settings


class Api(object):

    def __init__(self, store_id, access_token):
        self.base_url = 'https://{}.29next.store/api/admin/'.format(store_id)
        self.access_token = access_token

    def _build_url(self, path):
        return '{}{}'.format(self.base_url, path)

    def _default_headers(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token),
            'X-29next-API-Version': settings.STORE_API_VERSION,
        }
        return headers

    def _get(self, path):
        headers = self._default_headers()
        url = self._build_url(path)
        return requests.get(url, headers=headers)

    def _post(self, path, data):
        headers = self._default_headers()
        url = self._build_url(path)
        return requests.post(url, json=data, headers=headers)

    def _put(self, path, data):
        headers = self._default_headers()
        url = self._build_url(path)
        return requests.put(url, json=data, headers=headers)

    def _patch(self, path, data):
        headers = self._default_headers()
        url = self._build_url(path)
        return requests.patch(url, json=data, headers=headers)

    def create_location(self, name, address):
        path = 'locations/'
        data = {
            'name': name,
            'address': address,
            'callback_url': settings.LOCATION_CALLBACK_URL
        }
        return self._post(path, data)

    def get_locations(self):
        path = 'locations/'
        return self._get(path)

    def get_all_assigned_fulfillment_orders(self):
        path = 'assigned-fulfillment-orders/'
        return self._get(path)

    def get_requested_fulfillment_orders(self):
        path = 'assigned-fulfillment-orders/?assignment_status=fulfillment_requested'
        return self._get(path)

    def get_cancellation_requested_fulfillment_orders(self):
        path = 'assigned-fulfillment-orders/?assignment_status=cancellation_requested'
        return self._get(path)

    def accept_fulfillment_request(self, id, message):
        path = 'fulfillment-orders/{}/fulfillment-request/accept/'.format(id)
        data = {
            'message': message
        }
        return self._post(path, data)

    def reject_fulfillment_request(self, id, message):
        path = 'fulfillment-orders/{}/fulfillment-request/reject/'.format(id)
        data = {
            'message': message
        }
        return self._post(path, data)

    def accept_cancellation_request(self, id, message):
        path = 'fulfillment-orders/{}/cancellation-request/accept/'.format(id)
        data = {
            'message': message
        }
        return self._post(path, data)

    def reject_cancellation_request(self, id, message):
        path = 'fulfillment-orders/{}/cancellation-request/reject/'.format(id)
        data = {
            'message': message
        }
        return self._post(path, data)

    def create_fulfillment(
        self, fulfillment_order_id, tracking_code, carrier, carrier_other_name=None
    ):
        path = 'fulfillment-orders/{}/fulfillments/'.format(fulfillment_order_id)
        data = {
            'notify': True,
            'tracking_info': [
                {
                    'tracking_code': tracking_code,
                    'carrier': carrier
                }
            ]
        }
        if carrier_other_name:
            data['tracking_info'][0]['carrier_other_name'] = carrier_other_name

        return self._post(path, data)

    def create_webhook(self, events, name, target):
        path = 'webhooks/'
        data = {
            'events': events,
            'name': name,
            'target': target,
            'version': settings.STORE_API_VERSION,
            'secret_key': settings.WEBHOOK_SECRET
        }
        return self._post(path, data)
