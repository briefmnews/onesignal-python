"""Notification class."""
import json


class Notification(object):
    """Notification class."""
    SEGMENTS_MODE = 'segments'
    DEVICES_MODE = 'devices'
    FILTERS_MODE = 'filters'
    DEFAULT_LANGUAGE = 'en'
    NOTIFICATION_MODES = [SEGMENTS_MODE, DEVICES_MODE, FILTERS_MODE]
    IOS_BADGE_TYPE_NONE = 'None'
    IOS_BADGE_TYPE_SETTO = 'SetTo'
    IOS_BADGE_TYPE_INCREASE = 'Increase'
    IOS_BADGES_TYPES = [
        IOS_BADGE_TYPE_NONE, IOS_BADGE_TYPE_SETTO, IOS_BADGE_TYPE_INCREASE
    ]

    # Mode Settings
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.NOTIFICATION_MODES:
            raise ValueError('Unknown operation mode.')

        self._mode = value

    # Device mode properties
    @property
    def include_player_ids(self):
        return self._include_player_ids

    @include_player_ids.setter
    def include_player_ids(self, value):
        if self.mode != self.DEVICES_MODE:
            raise TypeError('Mode should be set to device.')

        if not isinstance(value, list):
            raise TypeError('Value must be a list.')

        self._include_player_ids = value

    # Common Parameters - App
    @property
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, value):
        self._app_id = value

    # Common Parameters - Content & Language
    @property
    def contents(self):
        return json.loads(self._contents)

    @contents.setter
    def contents(self, value):
        self._validate_content_dict(value)
        self._contents = json.dumps(value)

    @property
    def content_available(self):
        return self._content_available

    @content_available.setter
    def content_available(self, value):
        self._content_available = value

    @property
    def headings(self):
        return json.loads(self._headings)

    @headings.setter
    def headings(self, value):
        self._validate_content_dict(value)
        self._headings = json.dumps(value)

    @property
    def subtitle(self):
        return json.loads(self._subtitle)

    @subtitle.setter
    def subtitle(self, value):
        self._validate_content_dict(value)
        self._subtitle = json.dumps(value)

    # Common Parameters - Attachments
    @property
    def data(self):
        return json.loads(self._data)

    @data.setter
    def data(self, value):
        if isinstance(value, str):
            value = json.loads(value)

        if not isinstance(value, dict):
            raise TypeError('Value must be a dict.')

        self._data = json.dumps(value)

    # Common Parameters - Appearance
    @property
    def small_icon(self):
        return self._small_icon

    @small_icon.setter
    def small_icon(self, value):
        self._small_icon = str(value) if value is not None else None

    @property
    def large_icon(self):
        return self._large_icon

    @large_icon.setter
    def large_icon(self, value):
        self._large_icon = str(value) if value is not None else None

    @property
    def ios_badge_type(self):
        return self._ios_badge_type

    @ios_badge_type.setter
    def ios_badge_type(self, value):
        if value not in self.IOS_BADGES_TYPES:
            raise TypeError('Unknown badge type.')

        self._ios_badge_type = value

    @property
    def ios_badge_count(self):
        return self._ios_badge_count

    @ios_badge_count.setter
    def ios_badge_count(self, value):
        self._ios_badge_count = int(value)

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        if not isinstance(value, int):
            raise TypeError('Value must be an int.')
        if value < 0:
            raise ValueError('Value must be a non-negative number.')
        if value > 2419200:
            raise ValueError(
                'Value cannot be greater than 2419200 seconds (28 days).')

        self._ttl = value

    def __init__(self, app_id, mode=SEGMENTS_MODE):
        self.app_id = app_id
        self.mode = mode

        # Device defaults
        self._include_player_ids = []

        self._ttl = None

        # Common defaults
        self.contents = {'en': 'Default message.'}
        self.content_available = False
        self.headings = {}
        self.subtitle = {}
        self.send_after = None
        self.url = None
        self.data = {}
        self.small_icon = None
        self.large_icon = None
        self.chrome_icon = None
        self.ios_badge_type = self.IOS_BADGE_TYPE_NONE
        self.ios_badge_count = 0

    def _validate_content_dict(self, value):
        """
        Validates dicts used for content properties.
        Ex: headings, subtitle, contents.
        """
        if isinstance(value, str):
            value = json.loads(value)

        if not isinstance(value, dict):
            raise TypeError('Value must be a dict.')

        if len(value) > 0 and not value.get(self.DEFAULT_LANGUAGE, False):
            raise KeyError('Default language (%s) must be included.' % (
                self.DEFAULT_LANGUAGE))

        return True

    def get_payload_for_request(self):
        """
        Get the JSON data to be sent to /notifications post.
        """
        payload = {
            'app_id': self.app_id,
            # Should change when template/content_available support be done
            'contents': self.contents,
            'content_available': self.content_available
        }

        # Mode related settings
        if self.mode == self.DEVICES_MODE:
            payload.update({'include_player_ids': self.include_player_ids})

        # Common parameters
        if len(self.data) > 0:
            payload.update({'data': self.data})

        if len(self.headings) > 0:
            payload.update({'headings': self.headings})

        if len(self.subtitle) > 0:
            payload.update({'subtitle': self.subtitle})

        if self.send_after:
            payload.update({'send_after': self.send_after})

        if self.url:
            payload.update({'url': self.url})

        if self.small_icon:
            payload.update({'small_icon': self.small_icon})

        if self.large_icon:
            payload.update({'large_icon': self.large_icon})

        if self.chrome_icon:
            payload.update({'chrome_icon': self.chrome_icon})

        if self.ios_badge_count > 0:
            payload.update({
                'ios_badgeType': self.ios_badge_type,
                'ios_badgeCount': self.ios_badge_count
            })

        if self.ttl:
            payload.update({'ttl': self.ttl})

        return payload
