"""
Support for Lightpack remote.
"""
import asyncio
import logging
import socket
import sys
import traceback

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
import homeassistant.util.color as color_util
from distutils.version import StrictVersion
from homeassistant.components.light import (ATTR_BRIGHTNESS, ATTR_EFFECT,
                                            ATTR_HS_COLOR, DOMAIN,
                                            LIGHT_TURN_ON_SCHEMA,
                                            PLATFORM_SCHEMA,
                                            SUPPORT_BRIGHTNESS,
                                            SUPPORT_COLOR, SUPPORT_EFFECT,
                                            Light,
                                            preprocess_turn_on_alternatives)
from homeassistant.const import (CONF_API_KEY, CONF_HOST, CONF_NAME,
                                 CONF_PORT, EVENT_HOMEASSISTANT_STOP)
from typing import Tuple, List, Optional

# REQUIREMENTS = ['py-lightpack==2.1.0']
REQUIREMENTS = ["https://github.com/renemarc/py-lightpack/archive/"
                "feature/expand-api-command-set.tar.gz"
                "py-lightpack==2.1.0"]

_LOGGER = logging.getLogger(__name__)

DATA_LIGHTPACK = 'lightpack'

SERVICE_SET_STATE = 'lightpack_set_state'

SUPPORT_LIGHTPACK = SUPPORT_EFFECT

MODE_AMBILIGHT = 'ambilight'
MODE_MOODLAMP = 'moodlamp'
MODE_SOUNDVIZ = 'soundviz'

LIGHTPACK_MODE_LIST = [
    MODE_AMBILIGHT,
    MODE_MOODLAMP,
]

ICON = 'mdi:television'

DEFAULT_NAME = 'Lightpack'
DEFAULT_PORT = 3636

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

ATTR_API_VERSION = 'api_version'
ATTR_PERSIST = 'persist'
ATTR_POWER = 'power'
ATTR_ZONES = 'zones'

LIGHTPACK_SET_STATE_SCHEMA = LIGHT_TURN_ON_SCHEMA.extend({
    ATTR_POWER: cv.boolean,
    ATTR_ZONES: vol.All(cv.ensure_list, [cv.positive_int]),
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None) -> None:
    """Set up Lightpack remote."""
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    _LOGGER.debug("%s: async_setup_platform()", name)

    device = Lightpack(
        host=host,
        port=config.get(CONF_PORT),
        api_key=config.get(CONF_API_KEY),
        name=name,
    )
    async_add_entities([device], update_before_add=True)

    if DATA_LIGHTPACK not in hass.data:
        hass.data[DATA_LIGHTPACK] = dict()
    hass.data[DATA_LIGHTPACK][host] = device

    # Register the Lightpack set_state service call.
    async def async_service_handler(service) -> None:
        """Allow managing Lightpack without having to turn it on."""
        entity_ids = service.data.get('entity_id')
        if entity_ids:
            lights = [light
                      for light in hass.data[DATA_LIGHTPACK].values()
                      if light.entity_id in entity_ids]
        else:
            lights = hass.data[DATA_LIGHTPACK].values()

        tasks = []
        for light in lights:
            if service.service == SERVICE_SET_STATE:
                task = light.set_state(**service.data)
                tasks.append(hass.async_create_task(task))
        if tasks:
            await asyncio.wait(tasks, loop=hass.loop)

    hass.services.async_register(
        DOMAIN, SERVICE_SET_STATE, async_service_handler,
        schema=LIGHTPACK_SET_STATE_SCHEMA)

    # Listen for the stop event and cleanup.
    async def cleanup(event) -> None:
        """Remove listeners and close connections."""
        for service in [SERVICE_SET_STATE]:
            hass.services.async_remove(DOMAIN, service)
        await device.disconnect()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)


class Lightpack(Light):
    """Representation of Lightpack remote."""
    import lightpack

    def __init__(self, host, port=3636, api_key=None, name='Lightpack') -> \
            None:
        """Initialize the light."""
        _LOGGER.debug("%s: __init__", name)
        self._update = None
        self._control = None
        self._host = host
        self._port = port
        self._api_key = api_key
        self._name = name

        self._api_version = '1.4'
        self._attributes = {}
        self._available = False
        self._brightness = None
        self._effect = None
        self._effects = []
        self._icon = ICON
        self._hs = None
        self._locked = False
        self._mode = None
        self._state = None
        self._zones = None

    @property
    def api_version(self) -> Optional[str]:
        """Return the API version."""
        return self._api_version

    @property
    def available(self) -> bool:
        """Return True if available."""
        return self._available

    @property
    def brightness(self) -> Optional[int]:
        """Return the brightness."""
        return self._brightness

    @property
    def effect_list(self) -> List:
        """Return the list of supported effects (aka Lightpack profiles)."""
        return self._effects

    @property
    def effect(self) -> Optional[str]:
        """Return the current effect (aka Lightpack profile)."""
        return self._effect

    @property
    def hs_color(self) -> Optional[Tuple[float, float]]:
        """Return the hue and saturation color value."""
        return self._hs

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        if self.mode == MODE_AMBILIGHT:
            self._icon = 'mdi:video-input-hdmi'
        elif self.mode == MODE_MOODLAMP:
            self._icon = 'mdi:lava-lamp'
        elif self.mode == MODE_SOUNDVIZ:
            self._icon = 'mdi:music-box-outline'
        return self._icon

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if on."""
        return self._state

    @property
    def mode(self) -> Optional[str]:
        """Return the mode."""
        return self._mode

    @property
    def mode_list(self) -> List[str]:
        """Return the list of supported modes."""
        modes = LIGHTPACK_MODE_LIST
        if StrictVersion(self.api_version) >= StrictVersion('2.0'):
            modes = modes | MODE_SOUNDVIZ
        return modes

    @property
    def name(self) -> str:
        """Return the name of the light."""
        return self._name

    @property
    def state_attributes(self) -> dict:
        """Return the state attributes."""
        attr = super().state_attributes
        return {**attr, **self._attributes}

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        features = SUPPORT_LIGHTPACK
        api_version = StrictVersion(self.api_version)
        if api_version >= StrictVersion('1.5'):
            features = features | SUPPORT_BRIGHTNESS
        if api_version >= StrictVersion('2.2'):
            features = features | SUPPORT_COLOR
        return features

    @property
    def zones(self) -> Optional[int]:
        """Return the number of addressable lights."""
        return self._zones

    def get_brightness(self) -> Optional[int]:
        """Return current brightness."""
        try:
            brightness = self._update.getBrightness()
            self._brightness = int(brightness * 2.55)
            _LOGGER.debug("%s: get_brightness(); brightness: %s", self._name,
                          self._brightness)
        except self.lightpack.CommandFailedError:
            pass
        return self._brightness

    def get_color(self) -> Optional[Tuple[float, float]]:
        """Return current hue/saturation."""
        try:
            rgb = self._update.getColourAverage()
            if rgb:
                self._hs = color_util.color_RGB_to_hs(*rgb)
            else:
                self._hs = None
            _LOGGER.debug("%s: get_color(); rgb: %s; hs: %s", self._name,
                          rgb, self._hs)
        except self.lightpack.CommandFailedError:
            pass
        return self._hs

    def get_effect(self) -> Optional[str]:
        """Return current effect (aka Lightpack profile)."""
        try:
            self._effect = self._update.getProfile()
            _LOGGER.debug("%s: get_effect(); profile: %s", self._name,
                          self._effect)
        except self.lightpack.CommandFailedError:
            pass
        return self._effect

    def get_effects(self) -> List[str]:
        """List available effects (aka Lightpack profiles)."""
        try:
            self._effects = self._update.getProfiles(fresh=False)
            _LOGGER.debug("%s: get_effects(); profiles: %s", self._name,
                          self._effects)
        except self.lightpack.CommandFailedError:
            pass
        return self._effects

    def get_mode(self) -> Optional[str]:
        """Return current mode."""
        try:
            self._mode = self._update.getMode()
            _LOGGER.debug("%s: get_mode(); mode: %s", self._name, self._mode)
        except self.lightpack.CommandFailedError:
            pass
        return self._mode

    def get_state(self) -> Optional[bool]:
        """Return Lightpack status."""
        try:
            status = self._update.getStatus()
        except ConnectionResetError:
            self._available = False
            self._state = None
        except self.lightpack.CommandFailedError:
            self._available = False
            self._state = None
        except Exception as e:
            _LOGGER.error("%s, %s", self._name, e)
            _LOGGER.error("Unexpected error: %s",
                          traceback.format_exception(*sys.exc_info()))
            self._available = False
            self._state = None
        else:
            _LOGGER.debug("%s: get_state(); state: %s", self._name, status)
            self._available = True
            if status == 'on':
                self._state = True
            elif status == 'off':
                self._state = False
            else:
                self._available = False
                self._state = None
        return self._state

    def get_zones(self) -> Optional[int]:
        """Return number of addressable lights."""
        try:
            self._zones = self._update.getCountLeds(fresh=False)
            _LOGGER.debug("%s: get_zones(); zones: %s", self._name, self._zones)
        except self.lightpack.CommandFailedError:
            pass
        else:
            self._attributes[ATTR_ZONES] = self.zones
        return self._zones

    def set_brightness(self, brightness) -> None:
        """Set brightness."""
        brightness_pct = int(brightness / 2.55)
        _LOGGER.debug("%s: set_brightness(); brightness: %s; pct: %s",
                      self._name, brightness, brightness_pct)
        locked = False
        if not self._locked:
            self.lock()
            locked = True
        try:
            self._control.setBrightness(brightness_pct)
        except self.lightpack.CommandFailedError:
            pass
        if locked:
            self.unlock()

    def set_color(self, rgb, kwargs) -> None:
        """Change color for all lights or a select set."""
        zones = kwargs.get(ATTR_ZONES)
        _LOGGER.debug("%s: set_color(); color: %s; zones: %s", self._name,
                      rgb, zones)
        locked = False
        if not self._locked:
            self.lock()
            locked = True
        try:
            self.persist()
            if zones is None:
                self._control.setColourToAll(rgb)
            else:
                real_zones = [x for x in set(zones) if x < self.zones]
                if len(real_zones) < len(zones):
                    _LOGGER.warning("Maximum %s zero-indexed zones can be "
                                    "addressed, out of reach zones were "
                                    "dropped.", self.zones)
                colors = [(k, rgb) for k in real_zones]
                if colors:
                    self._control.setColours(*colors)
        except self.lightpack.CommandFailedError:
            pass
        if locked:
            self.unlock()

    def set_effect(self, effect) -> None:
        """Activate effect (aka Lightpack profile)."""
        _LOGGER.debug("%s: set_effect(); profile: %s", self._name, effect)
        locked = False
        if not self._locked:
            self.lock()
            locked = True
        try:
            self._control.setProfile(effect)
            if StrictVersion(self.api_version) >= StrictVersion('2.2') and \
                    self._control.getPersistence() == 'on':
                self.unpersist()
        except self.lightpack.CommandFailedError:
            pass
        if locked:
            self.unlock()

    def lock(self) -> None:
        """Get exclusive control of Lightpack."""
        _LOGGER.debug("%s: lock()", self._name)
        try:
            self._control.lock()
        except self.lightpack.CommandFailedError:
            pass
        else:
            self._locked = True

    def unlock(self) -> None:
        """Release exclusive control of Lightpack."""
        _LOGGER.debug("%s: unlock()", self._name)
        try:
            self._control.unlock()
        except self.lightpack.CommandFailedError:
            pass
        else:
            self._locked = False

    def persist(self) -> None:
        """Make color changes stick."""
        _LOGGER.debug("%s: persist()", self._name)
        try:
            self._control.persist()
        except self.lightpack.CommandFailedError:
            pass
        else:
            self._attributes[ATTR_PERSIST] = True

    def unpersist(self) -> None:
        """Release Lightpack color changes."""
        _LOGGER.debug("%s: unpersist()", self._name)
        try:
            self._control.unpersist()
        except self.lightpack.CommandFailedError:
            pass
        else:
            self._attributes[ATTR_PERSIST] = False

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the lights on."""
        _LOGGER.debug("%s: turn_on(): args: %s", self._name, kwargs)
        kwargs[ATTR_POWER] = True
        await self.hass.async_create_task(self.set_state(**kwargs))

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the lights on."""
        _LOGGER.debug("%s: turn_off()", self._name)
        kwargs[ATTR_POWER] = False
        await self.hass.async_create_task(self.set_state(**kwargs))

    async def set_state(self, **kwargs) -> None:
        """Set attributes on the Lightpack and turn it on/off."""
        preprocess_turn_on_alternatives(kwargs)

        effect = kwargs.get(ATTR_EFFECT)
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        hs_color = kwargs.get(ATTR_HS_COLOR)
        power = kwargs.get(ATTR_POWER)

        self.lock()

        if effect is not None:
            _LOGGER.debug("%s: set_state(); set_effect(); effect: %s)",
                          self._name, effect)
            self.set_effect(effect)

        if brightness is not None:
            _LOGGER.debug("%s: set_state(); set_brightness(); brightness: %s)",
                          self._name, brightness)
            self.set_brightness(brightness)

        if hs_color is not None:
            rgb = color_util.color_hs_to_RGB(*hs_color)
        else:
            rgb = None
        if rgb is not None:
            _LOGGER.debug("%s: set_state(); set_color(); hs: %s; rgb: %s)",
                          self._name, hs_color, rgb)
            self.set_color(rgb, kwargs)

        if power is not None:
            if power:
                self._control.turnOn()
            else:
                self._control.turnOff()

        self.unlock()

    async def async_update(self) -> None:
        """Update Lightpack status."""
        _LOGGER.debug("%s: update()", self._name)
        if not self.available:
            try:
                await self.connect()
            except socket.error:
                await self.disconnect()
                return

        self.get_state()
        if not self.available:
            return False

        self.get_effects()
        self.get_effect()
        self.get_mode()
        self.get_zones()

        if self.supported_features & SUPPORT_BRIGHTNESS:
            self.get_brightness()

        if self.supported_features & SUPPORT_COLOR:
            self.get_color()

        _LOGGER.debug("%s: update(); brightness: %s; mode: %s; color: %s",
                      self._name, self._brightness, self._mode, self._hs)

    async def connect(self) -> bool:
        """Connect to Lightpack."""
        _LOGGER.debug("%s: connect()", self._name)
        import lightpack
        try:
            self._update = lightpack.Lightpack(host=self._host,
                                               port=self._port,
                                               api_key=self._api_key)
            self._update.connect()
            self._control = lightpack.Lightpack(host=self._host,
                                                port=self._port,
                                                api_key=self._api_key)
            self._control.connect()
            self._available = True
        except self.lightpack.CannotConnectError as e:
            _LOGGER.error("%s:connect(); result: %s", self._name, repr(e))
            _LOGGER.error("Unexpected error: %s", traceback.format_exception(
                *sys.exc_info()))
            self._available = False
        else:
            api_version = self._update.getApiVersion()
            if api_version is not None:
                self._api_version = str(api_version)
            self._attributes[ATTR_API_VERSION] = self.api_version
            if StrictVersion(self.api_version) >= StrictVersion('2.2'):
                self._attributes[ATTR_PERSIST] = False
        return self.available

    async def disconnect(self) -> None:
        """Return Lightpack to defaults and disconnect."""
        _LOGGER.debug("%s: disconnect()", self._name)
        try:
            if self._locked:
                self._control.unpersist()
                self._control.unlock()
            self._control.disconnect()
            self._update.disconnect()
        except self.lightpack.CannotConnectError as e:
            _LOGGER.error("%s:disconnect(); result: %s", self._name, repr(e))
            _LOGGER.error("Unexpected error: %s", traceback.format_exception(
                *sys.exc_info()))
        self._available = False
