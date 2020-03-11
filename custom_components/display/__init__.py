"""
Home Assistant Display Component

Copyright (c) Darryl Ross, darryl@afoyi.com

Please see https://github.com/daemondazz/homeassistant-displays for instructions and latest updates.
"""

import logging
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.group import (
    ENTITY_ID_FORMAT as GROUP_ENTITY_ID_FORMAT
)
from homeassistant.const import (
    MAJOR_VERSION, MINOR_VERSION,
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF, SERVICE_TURN_ON,
    STATE_ON
)
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA, PLATFORM_SCHEMA_BASE
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.loader import bind_hass


_LOGGER = logging.getLogger(__name__)

DOMAIN = 'display'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

GROUP_NAME_ALL_DISPLAYS = 'all displays'
ENTITY_ID_ALL_DISPLAYS = GROUP_ENTITY_ID_FORMAT.format('all_displays')

SCAN_INTERVAL = timedelta(seconds=30)

ATTR_BRIGHTNESS = 'brightness'
ATTR_URL = 'url'

SERVICE_LOAD_URL = 'load_url'
SERVICE_SET_BRIGHTNESS = 'set_brightness'

SUPPORT_TURN_ON = 1
SUPPORT_TURN_OFF = 2
SUPPORT_LOAD_URL = 4
SUPPORT_SET_BRIGHTNESS = 8

DISPLAY_DEVICE_SCHEMA = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
})
DISPLAY_DEVICE_LOAD_URL_SCHEMA = DISPLAY_DEVICE_SCHEMA.extend({
    vol.Required(ATTR_URL): cv.string,
})
DISPLAY_DEVICE_SET_BRIGHTNESS_SCHEMA = DISPLAY_DEVICE_SCHEMA.extend({
    vol.Optional(ATTR_BRIGHTNESS, default=None):
        vol.Any(
            vol.All(str, vol.Length(min=0, max=3)),
            vol.All(int, vol.Range(min=0, max=255))
        )
})


@bind_hass
def is_on(hass, entity_id=None):
    entity_id = entity_id or ENTITY_ID_ALL_DISPLAYS
    return hass.states.is_state(entity_id, STATE_ON)


async def async_setup(hass, config):
    if (MAJOR_VERSION, MINOR_VERSION) >= (0, 104):
        component = hass.data[DOMAIN] = EntityComponent(
            _LOGGER, DOMAIN, hass, SCAN_INTERVAL)
    else:
        component = hass.data[DOMAIN] = EntityComponent(
            _LOGGER, DOMAIN, hass, SCAN_INTERVAL, GROUP_NAME_ALL_DISPLAYS)

    await component.async_setup(config)

    component.async_register_entity_service(
        SERVICE_LOAD_URL, DISPLAY_DEVICE_LOAD_URL_SCHEMA,
        'async_load_url', [SUPPORT_LOAD_URL]
    )

    component.async_register_entity_service(
        SERVICE_SET_BRIGHTNESS, DISPLAY_DEVICE_SET_BRIGHTNESS_SCHEMA,
        'async_set_brightness', [SUPPORT_SET_BRIGHTNESS]
    )

    component.async_register_entity_service(
        SERVICE_TURN_ON, DISPLAY_DEVICE_SCHEMA,
        'async_turn_on', [SUPPORT_TURN_ON]
    )

    component.async_register_entity_service(
        SERVICE_TURN_OFF, DISPLAY_DEVICE_SCHEMA,
        'async_turn_off', [SUPPORT_TURN_OFF]
    )

    return True


class DisplayDevice(ToggleEntity):
    @property
    def supported_features(self):
        return 0

    @property
    def status(self):
        return None

    @property
    def battery_level(self):
        return None

    def load_url(self, url):
        raise NotImplementedError()

    def async_load_url(self, url):
        return self.hass.async_add_job(self.load_url, url)

    def set_brightness(self, brightness):
        raise NotImplementedError()

    def async_set_brightness(self, brightness):
        return self.hass.async_add_job(self.set_brightness, brightness)

    def turn_off(self):
        raise NotImplementedError()

    def async_turn_off(self):
        return self.hass.async_add_job(self.turn_off)

    def turn_on(self):
        raise NotImplementedError()

    def async_turn_on(self):
        return self.hass.async_add_job(self.turn_on)
