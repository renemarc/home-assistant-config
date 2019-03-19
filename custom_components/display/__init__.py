import asyncio
import logging
from datetime import timedelta
from functools import partial

import voluptuous as vol

import homeassistant.core as ha
from homeassistant.const import (
    ATTR_ENTITY_ID, SERVICE_TURN_OFF, SERVICE_TURN_ON, STATE_ON
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.config_validation import (  # noqa
    PLATFORM_SCHEMA, PLATFORM_SCHEMA_BASE)
from homeassistant.loader import bind_hass

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'display'
ENTITY_ID_FORMAT = DOMAIN + '.{}'
GROUP_NAME_ALL_DISPLAYS = 'all displays'
SCAN_INTERVAL = timedelta(seconds=30)

DISPLAY_SERVICE_SCHEMA = vol.Schema({
    ATTR_ENTITY_ID: cv.entity_ids,
})

SERVICE_TO_METHOD = {
    SERVICE_TURN_ON: {'method': 'async_turn_on'},
    SERVICE_TURN_OFF: {'method': 'async_turn_off'},
}

SUPPORT_TURN_ON = 1
SUPPORT_TURN_OFF = 2
SUPPORT_SEND_COMMAND = 4


@bind_hass
def is_on(hass, entity_id=None):
    entity_id = entity_id or ENTITY_ID_ALL_DISPLAYS
    return hass.states.is_state(entity_id, STATE_ON)


@bind_hass
def send_command(hass, command, params=None, entity_id=None):
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    data[ATTR_COMMAND] = command
    if params is not None:
        data[ATTR_PARAMS] = params
    hass.services.call(DOMAIN, SERVICE_SEND_COMMAND, data)


@bind_hass
def turn_on(hass, entity_id=None):
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    hass.services.call(DOMAIN, SERVICE_TURN_ON, data)


@bind_hass
def turn_off(hass, entity_id=None):
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    hass.services.call(DOMAIN, SERVICE_TURN_OFF, data)


@asyncio.coroutine
def async_setup(hass, config):
    component = EntityComponent(
        _LOGGER, DOMAIN, hass, SCAN_INTERVAL, GROUP_NAME_ALL_DISPLAYS)

    yield from component.async_setup(config)

    @asyncio.coroutine
    def async_handle_display_service(service):
        method = SERVICE_TO_METHOD.get(service.service)
        target_displays = component.async_extract_from_service(service)
        params = service.data.copy()
        params.pop(ATTR_ENTITY_ID, None)

        update_tasks = []
        for display in target_displays:
            yield from getattr(display, method['method'])(**params)
            if not display.should_poll:
                continue
            update_tasks.append(display.async_update_ha_state(True))

        if update_tasks:
            yield from asyncio.wait(update_tasks, loop=hass.loop)

    for service in SERVICE_TO_METHOD:
        schema = SERVICE_TO_METHOD[service].get(
            'schema', DISPLAY_SERVICE_SCHEMA)
        hass.services.async_register(
            DOMAIN, service, async_handle_display_service,
            schema=schema)

    return True


class DisplayDevice(ToggleEntity):
    @property
    def supported_features(self):
        raise NotImplementedError()

    @property
    def status(self):
        return None

    @property
    def battery_level(self):
        return None

    def turn_on(self, **kwargs):
        raise NotImplementedError()

    def async_turn_on(self, **kwargs):
        return self.hass.async_add_job(partial(self.turn_on, **kwargs))

    def turn_off(self, **kwargs):
        raise NotImplementedError()

    def async_turn_off(self, **kwargs):
        return self.hass.async_add_job(partial(self.turn_off, **kwargs))
