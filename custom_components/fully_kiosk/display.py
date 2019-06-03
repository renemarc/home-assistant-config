"""
Support for Fully Kiosk Browser
"""

from datetime import timedelta
import logging
import requests
import voluptuous as vol

from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_PORT,
    STATE_OFF, STATE_ON, STATE_UNKNOWN
)
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

from ..display import (                                                     # pylint: disable=relative-beyond-top-level
    DisplayDevice,
    ATTR_BRIGHTNESS,
    SUPPORT_LOAD_URL, SUPPORT_SET_BRIGHTNESS, SUPPORT_TURN_OFF, SUPPORT_TURN_ON,
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'fully_kiosk'

ATTR_MESSAGE = 'message'
ATTR_LOCALE = 'locale'

DEFAULT_LOCALE = 'en'
DEFAULT_NAME = 'Fully Kiosk Browser'
DEFAULT_PORT = 2323

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=5)

SERVICE_LOAD_START_URL = 'load_start_url'
SERVICE_SAY = 'say'
SERVICE_SCREENSAVER_START = 'screensaver_start'
SERVICE_SCREENSAVER_STOP = 'screensaver_stop'
SERVICE_SET_SCREENSAVER_BRIGHTNESS = 'set_screensaver_brightness'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_PASSWORD): cv.string
})

SCHEMA_SERVICE_LOAD_START_URL = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
})
SCHEMA_SERVICE_SCREENSAVER_START = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
})
SCHEMA_SERVICE_SCREENSAVER_STOP = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
})
SCHEMA_SERVICE_SAY = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
    vol.Required(ATTR_MESSAGE): cv.string,
    vol.Optional(ATTR_LOCALE, default=DEFAULT_LOCALE): cv.string
})
SCHEMA_SERVICE_SET_SCREENSAVER_BRIGHTNESS = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
    vol.Optional(ATTR_BRIGHTNESS, default=255):
        vol.Any(
            vol.All(str, vol.Length(min=0, max=0)),
            vol.All(int, vol.Range(min=0, max=255))
        )
})


def setup_platform(hass, config, add_devices, discovery_info=None):                   # pylint: disable=unused-argument
    def service_handler(call):
        entity_ids = call.data.get(ATTR_ENTITY_ID)
        if entity_ids:
            devices = [device for device in hass.data[DOMAIN]
                       if device.entity_id in entity_ids]
        else:
            devices = hass.data[DOMAIN]
        for device in devices:
            if call.service == SERVICE_LOAD_START_URL:
                device.load_start_url()
            elif call.service == SERVICE_SAY:
                device.tts(call.data[ATTR_MESSAGE], call.data[ATTR_LOCALE])
            elif call.service == SERVICE_SCREENSAVER_START:
                device.turn_screensaver_on()
            elif call.service == SERVICE_SCREENSAVER_STOP:
                device.turn_screensaver_off()
            elif call.service == SERVICE_SET_SCREENSAVER_BRIGHTNESS:
                device.set_screensaver_brightness(call.data[ATTR_BRIGHTNESS])

    _LOGGER.info("Setting up FullyKioskDevice for %s at %s:%s",
                 config.get(CONF_NAME, DEFAULT_NAME),
                 config.get(CONF_HOST), config.get(CONF_PORT, DEFAULT_PORT))

    if not DOMAIN in hass.data:
        hass.data[DOMAIN] = []

    device = FullyKioskDevice(config.get(CONF_NAME, DEFAULT_NAME),
                              config.get(CONF_HOST),
                              config.get(CONF_PORT, DEFAULT_PORT),
                              config.get(CONF_PASSWORD))
    hass.data[DOMAIN].append(device)
    add_devices([device], True)

    hass.services.register(
        DOMAIN, SERVICE_SAY, service_handler,
        schema=SCHEMA_SERVICE_SAY)

    hass.services.register(
        DOMAIN, SERVICE_LOAD_START_URL, service_handler,
        schema=SCHEMA_SERVICE_LOAD_START_URL)

    hass.services.register(
        DOMAIN, SERVICE_SCREENSAVER_START, service_handler,
        schema=SCHEMA_SERVICE_SCREENSAVER_START)

    hass.services.register(
        DOMAIN, SERVICE_SCREENSAVER_STOP, service_handler,
        schema=SCHEMA_SERVICE_SCREENSAVER_STOP)

    hass.services.register(
        DOMAIN, SERVICE_SET_SCREENSAVER_BRIGHTNESS, service_handler,
        schema=SCHEMA_SERVICE_SET_SCREENSAVER_BRIGHTNESS)


class FullyKioskDevice(DisplayDevice):
    def __init__(self, name, host, port, password):
        self.password = password
        self.url = 'http://{}:{}/'.format(host, port)

        self._name = name
        self._attributes = {}
        self._state = STATE_UNKNOWN

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORT_LOAD_URL | SUPPORT_SET_BRIGHTNESS | SUPPORT_TURN_OFF | SUPPORT_TURN_ON

    def load_start_url(self):
        self._send_command(command='loadStartURL')

    def load_url(self, url):
        self._send_command(command='loadURL', url=str(url))

    def set_brightness(self, brightness):
        self._send_command(command='setStringSetting', key='screenBrightness', value=str(brightness))

    def set_screensaver_brightness(self, brightness):
        self._send_command(command='setStringSetting', key='screensaverBrightness', value=str(brightness))

    def turn_off(self):
        self._send_command(command='screenOff')

    def turn_on(self):
        self._send_command(command='screenOn')

    def turn_screensaver_on(self):
        self._send_command(command='startScreensaver')

    def turn_screensaver_off(self):
        self._send_command(command='stopScreensaver')

    def tts(self, message, locale):
        self._send_command(command='textToSpeech', text=message, locale=locale)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        try:
            data = self._send_command('deviceInfo')
        except OSError:
            return False

        if 'status' in data and data['status'] == 'Error':
            _LOGGER.error(data['statustext'])
            return False

        self._state = (STATE_OFF, STATE_ON)[data['isScreenOn']]
        self._attributes = {
            'manufacturer': data['deviceManufacturer'],
            'model': data['deviceModel'],
            'device_id': data['deviceID'],
            'mac_address': data['mac'],
            'version': data['appVersionName'],
            'page': data['currentPage'],
            'battery_charging': data['plugged'],
            'battery_level': data['batteryLevel'],
            'display_resolution': '{}x{}'.format(data['displayWidthPixels'], data['displayHeightPixels']),
            'brightness': data['screenBrightness'],
            'kiosk_mode': data['kioskMode'],
            'maintenance_mode': data['maintenanceMode'],
            'screensaver_on': (data['currentFragment'] == 'screensaver'),
        }
        return True

    def _send_command(self, command, **payload):
        _LOGGER.debug("Sending %s command to %s", command, self.url)
        payload.update({
            'cmd': command,
            'password': self.password,
            'type': 'json',
        })
        response = requests.get(self.url, params=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {
            'status': 'Error',
            'statustext': 'Receieved HTTP {} from server'.format(response.status_code),
        }
