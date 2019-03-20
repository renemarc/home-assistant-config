"""
Support for Fully Kiosk Browser
"""

from datetime import timedelta
import logging
import requests
import voluptuous as vol

from homeassistant.const import (ATTR_ENTITY_ID,
                                 CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_PORT,
                                 STATE_OFF, STATE_ON, STATE_UNKNOWN)
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

from ..display import (
    DisplayDevice, DOMAIN,
    SUPPORT_TURN_OFF, SUPPORT_TURN_ON
)

_LOGGER = logging.getLogger(__name__)

ATTR_BRIGHTNESS = 'brightness'
ATTR_MESSAGE = 'message'
ATTR_LOCALE = 'locale'
ATTR_URL = 'url'

DEFAULT_LOCALE = 'en'
DEFAULT_NAME = 'Fully Kiosk Browser'
DEFAULT_PORT = 2323

DATA_ENTITIES = 'fully_kiosk_entities'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_PASSWORD): cv.string
})

NO_PARAMETERS_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
})

SCHEMA_SERVICE_LOAD_START_URL = NO_PARAMETERS_SCHEMA
SCHEMA_SERVICE_SCREENSAVER_START = NO_PARAMETERS_SCHEMA
SCHEMA_SERVICE_SCREENSAVER_STOP = NO_PARAMETERS_SCHEMA

SCHEMA_SERVICE_LOAD_URL = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
    vol.Required(ATTR_URL): cv.string,
})

SCHEMA_SERVICE_SAY = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
    vol.Required(ATTR_MESSAGE): cv.string,
    vol.Optional(ATTR_LOCALE, default=DEFAULT_LOCALE): cv.string
})

SCHEMA_SERVICE_SET_BRIGHTNESS = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
    vol.Optional(ATTR_BRIGHTNESS, default=None):
        vol.Any(
            vol.All(str, vol.Length(min=0, max=0)),
            vol.All(int, vol.Range(min=0, max=255))
        )
})

SUPPORT_FULLYKIOSK = SUPPORT_TURN_OFF | SUPPORT_TURN_ON

SERVICE_LOAD_URL = 'fullykiosk_load_url'
SERVICE_LOAD_START_URL = 'fullykiosk_load_start_url'
SERVICE_SAY = 'fullykiosk_say'
SERVICE_SCREENSAVER_START = 'fullykiosk_screensaver_start'
SERVICE_SCREENSAVER_STOP = 'fullykiosk_screensaver_stop'
SERVICE_SET_BRIGHTNESS = 'fullykiosk_set_brightness'
SERVICE_SET_SCREENSAVER_BRIGHTNESS = 'fullykiosk_set_screensaver_brightness'


def setup_platform(hass, config, add_devices, discovery_info=None):
    def service_handler(service):
        """Handle service calls."""
        entity_ids = service.data.get(ATTR_ENTITY_ID)

        if entity_ids:
            devices = [device for device in hass.data[DATA_ENTITIES] if device.entity_id in entity_ids]
        else:
            devices = hass.data[DATA_ENTITIES]

        for device in devices:
            if service.service == SERVICE_LOAD_START_URL:
                device.load_start_url()

            if service.service == SERVICE_LOAD_URL:
                device.load_url(service.data[ATTR_URL])

            if service.service == SERVICE_SAY:
                device.tts(service.data[ATTR_MESSAGE], service.data[ATTR_LOCALE])

            if service.service == SERVICE_SCREENSAVER_START:
                device.turn_screensaver_on()

            if service.service == SERVICE_SCREENSAVER_STOP:
                device.turn_screensaver_off()

            if service.service == SERVICE_SET_BRIGHTNESS:
                device.set_brightness(service.data[ATTR_BRIGHTNESS])

            if service.service == SERVICE_SET_SCREENSAVER_BRIGHTNESS:
                device.set_screensaver_brightness(service.data[ATTR_BRIGHTNESS])

            device.schedule_update_ha_state(True)

    fully_kiosk_device = FullyKioskDevice(config.get(CONF_NAME),
                                          config.get(CONF_HOST),
                                          config.get(CONF_PORT),
                                          config.get(CONF_PASSWORD))

    # Manage entity cache for service handler
    if DATA_ENTITIES not in hass.data:
        hass.data[DATA_ENTITIES] = []

    if fully_kiosk_device not in hass.data[DATA_ENTITIES]:
        hass.data[DATA_ENTITIES].append(fully_kiosk_device)
        add_devices([fully_kiosk_device])

    hass.services.register(DOMAIN,
                           SERVICE_LOAD_START_URL,
                           service_handler,
                           schema=SCHEMA_SERVICE_LOAD_START_URL)
    hass.services.register(DOMAIN,
                           SERVICE_LOAD_URL,
                           service_handler,
                           schema=SCHEMA_SERVICE_LOAD_URL)
    hass.services.register(DOMAIN,
                           SERVICE_SAY,
                           service_handler,
                           schema=SCHEMA_SERVICE_SAY)
    hass.services.register(DOMAIN,
                           SERVICE_SCREENSAVER_START,
                           service_handler,
                           schema=SCHEMA_SERVICE_SCREENSAVER_START)
    hass.services.register(DOMAIN,
                           SERVICE_SCREENSAVER_STOP,
                           service_handler,
                           schema=SCHEMA_SERVICE_SCREENSAVER_STOP)
    hass.services.register(DOMAIN,
                           SERVICE_SET_BRIGHTNESS,
                           service_handler,
                           schema=SCHEMA_SERVICE_SET_BRIGHTNESS)
    hass.services.register(DOMAIN,
                           SERVICE_SET_SCREENSAVER_BRIGHTNESS,
                           service_handler,
                           schema=SCHEMA_SERVICE_SET_BRIGHTNESS)


class FullyKioskDevice(DisplayDevice):
    def __init__(self, name, host, port, password):
        self.password = password
        self.url = 'http://{}:{}/'.format(host, port)

        self._name = name
        self._attributes = {}
        self._brightness = None
        self._page = None
        self._state = STATE_UNKNOWN

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def name(self):
        return self._name

    @property
    def source(self):
        return self._page

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_FULLYKIOSK

    def load_start_url(self):
        self._send_command(command='loadStartURL')
        self.update()

    def load_url(self, url):
        self._send_command(command='loadURL', url=str(url))
        self.update()

    def set_brightness(self, brightness):
        self._send_command(command='setStringSetting', key='screenBrightness', value=str(brightness))
        self.update()

    def set_screensaver_brightness(self, brightness):
        self._send_command(command='setStringSetting', key='screensaverBrightness', value=str(brightness))
        self.update()

    def turn_off(self):
        self._send_command(command='screenOff')
        self.update()

    def turn_on(self):
        self._send_command(command='screenOn')
        self.update()

    def turn_screensaver_on(self):
        self._send_command(command='startScreensaver')
        self.update()

    def turn_screensaver_off(self):
        self._send_command(command='stopScreensaver')
        self.update()

    def tts(self, message, locale):
        self._send_command(command='textToSpeech', text=message, locale=locale)
        self.update()


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        try:
            data = self._send_command('deviceInfo').json()
        except OSError:
            return False

        if 'status' in data and data['status'] == 'Error':
            _LOGGER.error(data['statustext'])
            return False
        self._attributes = {
            'manufacturer': data['deviceManufacturer'],
            'model': data['deviceModel'],
            'device_id': data['deviceID'],
            'mac_address': data['mac'],
            'version': data['appVersionName'],
            'battery_level': data['batteryLevel'],
            'display_resolution': '{}x{}'.format(data['displayWidthPixels'], data['displayHeightPixels']),
            'kiosk_mode': data['kioskMode'],
            'maintenance_mode': data['maintenanceMode'],
            'screensaver_on': (data['currentFragment'] == 'screensaver'),
        }
        self._brightness = data['screenBrightness']
        self._page = data['currentPage']
        if data['isScreenOn']:
            self._state = STATE_ON
        else:
            self._state = STATE_OFF
        return True

    def _send_command(self, command, **kwargs):
        payload = {
            'cmd': command,
            'password': self.password,
            'type': 'json',
            **kwargs
        }

        return requests.get(self.url, params=payload)
