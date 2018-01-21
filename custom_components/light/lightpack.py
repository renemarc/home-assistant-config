import logging
import telnetlib

import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import Light, DOMAIN, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_API_KEY
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTR_NAME = 'profile'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.Optional(CONF_API_KEY): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    # Assign configuration variables. The configuration check takes care they are present.
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    api_key = config.get(CONF_API_KEY)

    # Add device
    lightpack = Lightpack(host, port, api_key)
    add_devices([lightpack])

    def set_profile(call):
        """Instruct the light to change profile."""
        profile = call.data[ATTR_NAME]
        lightpack.set_lightpack(True, profile)

    hass.services.register(DOMAIN, set_profile.__name__, set_profile)

class Lightpack(Light):
    """Representation of a Lightpack"""
    def __init__(self, host, port, api_key):
        """Initialize a Lightpack."""
        self._host = host
        self._port = port
        self._api_key = api_key
        self._state = None

    @property
    def name(self):
        """Return the display name of this light."""
        return 'Lightpack'

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return 'mdi:television-guide'

    @property
    def is_on(self):
        """Return true if light is on."""
        try:
            telnet = telnetlib.Telnet(self._host, self._port)
            if (self._api_key != None):
                telnet.write(("apikey:" + self._api_key + "\n").encode('ascii'))
                telnet.read_until(b"ok\n", timeout=0.2)
            telnet.write(("getstatus\n").encode('ascii'))
            self._state = telnet.read_until(b"\n", timeout=0.2).strip().replace(b"status:", b"") == b"on"
            telnet.close()
        except IOError as error:
            _LOGGER.error('Command "%s" failed with exception: %s', command, repr(error))
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self.set_lightpack(True)

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self.set_lightpack(False)

    def set_lightpack(self, enabled, profile = None):
        try:
            telnet = telnetlib.Telnet(self._host, self._port)
            if (self._api_key != None):
                telnet.write(("apikey:" + self._api_key + "\n").encode('ascii'))
                telnet.read_until(b"\n", timeout=0.2)
            telnet.write(("lock\n").encode('ascii'))
            telnet.read_until(b"\n", timeout=0.2)
            if (enabled == True):
                telnet.write(("setstatus:on\n").encode('ascii'))
                if (profile != None):
                    telnet.read_until(b"\n", timeout=0.2)
                    telnet.write(("setprofile:" + profile + "\n").encode('ascii'))
                    _LOGGER.error('lightpack profile set to : ' + profile)
            else:
                telnet.write(("setstatus:off\n").encode('ascii'))
            telnet.read_until(b"\n", timeout=0.2)
            telnet.write(("unlock\n").encode('ascii'))
            telnet.read_until(b"\n", timeout=0.2)
            telnet.close()
            self._state = enabled
        except IOError as error:
            _LOGGER.error('Command "%s" failed with exception: %s', command, repr(error))
            self._state = False
            return None

    def update(self):
        """Periodically check to see if the light is on."""
        self._state = self.is_on
