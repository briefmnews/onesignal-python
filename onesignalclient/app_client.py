"""OneSignal App Client class."""
from .base_client import OneSignalBaseClient


class OneSignalAppClient(OneSignalBaseClient):
    """OneSignal Client."""
    ENDPOINTS = {
        'notifications': 'notifications',
        'devices': 'players',
        'csv_export': 'players/csv_export'
    }

    AVAILABLE_EXTRA_FIELDS = ['location', 'country', 'rooted']

    def __init__(self, app_id, app_api_key):
        """
        Initializes the OneSignal Client.

        :param app_id: OneSignal App ID.
        Found under OneSignal Dashboard > App Settings > Keys & IDs
        :type app_id: string
        :param app_api_key: Application REST API key.
        Found under OneSignal Dashboard > App Settings > Keys & IDs
        :type app_api_key: string
        """
        self.app_id = app_id
        self.app_api_key = app_api_key
        self.mode = self.MODE_APP

    def get_headers(self):
        """
        Build default headers for requests.
        :return: Returns dict which contains the headers
        """
        return self._get_headers()

    def create_notification(self, payload):
        """
        Creates a new notification.
        :param payload: the payload of the notification to create
        """
        return self.post(self._url(self.ENDPOINTS['notifications']),
                         payload=payload)

    def cancel_notification(self, notification_id):
        """
        Cancel a notification.
        :param notification_id: Notification identifier
        """
        endpoint = '{endpoint}/{nid}?app_id={app_id}'.format(
            endpoint=self.ENDPOINTS['notifications'],
            nid=notification_id,
            app_id=self.app_id
        )
        return self.delete(self._url(endpoint))

    def csv_export(self, extra_fields=[]):
        """
        Request a CSV export from OneSignal.
        :return: Returns the request result.
        """
        payload = {'extra_fields': []}

        if isinstance(extra_fields, list) and len(extra_fields) > 0:
            payload['extra_fields'] = [
                x for x in extra_fields if x in self.AVAILABLE_EXTRA_FIELDS
            ]

        endpoint = '{endpoint}?app_id={app_id}'.format(
            endpoint = self.ENDPOINTS['csv_export'],
            app_id=self.app_id
        )
        return self.post(self._url(endpoint), payload=payload)
