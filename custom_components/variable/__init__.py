import asyncio
import logging
import json

import voluptuous as vol

from homeassistant.const import (CONF_NAME, ATTR_ICON)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import template
from homeassistant.exceptions import TemplateError
from homeassistant.loader import bind_hass
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'variable'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

CONF_ATTRIBUTES = "attributes"
CONF_VALUE = "value"
CONF_RESTORE = "restore"

ATTR_VARIABLE = "variable"
ATTR_VALUE = 'value'
ATTR_VALUE_TEMPLATE = 'value_template'
ATTR_ATTRIBUTES = "attributes"
ATTR_ATTRIBUTES_TEMPLATE = "attributes_template"
ATTR_REPLACE_ATTRIBUTES = "replace_attributes"

SERVICE_SET_VARIABLE = "set_variable"
SERVICE_SET_VARIABLE_SCHEMA = vol.Schema({
    vol.Required(ATTR_VARIABLE): cv.string,
    vol.Optional(ATTR_VALUE): cv.match_all,
    vol.Optional(ATTR_VALUE_TEMPLATE): cv.template,
    vol.Optional(ATTR_ATTRIBUTES): dict,
    vol.Optional(ATTR_ATTRIBUTES_TEMPLATE): cv.template,
    vol.Optional(ATTR_REPLACE_ATTRIBUTES): cv.boolean
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.Any({
            vol.Optional(CONF_NAME): cv.string,
            vol.Optional(CONF_VALUE): cv.match_all,
            vol.Optional(CONF_ATTRIBUTES): dict,
            vol.Optional(CONF_RESTORE): cv.boolean,
        }, None)
    })
}, extra=vol.ALLOW_EXTRA)

@bind_hass
def set_variable(hass, variable, value, value_template, attributes, attributes_template, replace_attributes):
    """Set input_boolean to True."""
    hass.services.call(DOMAIN, SERVICE_SET_VARIABLE, {
        ATTR_VARIABLE: variable,
        ATTR_VALUE: value,
        ATTR_VALUE_TEMPLATE: value_template,
        ATTR_ATTRIBUTES: attributes,
        ATTR_ATTRIBUTES_TEMPLATE: attributes_template,
        ATTR_REPLACE_ATTRIBUTES: replace_attributes,
    })

async def async_setup(hass, config):
    """Set up variables."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = []

    for variable_id, variable_config in config[DOMAIN].items():
        if not variable_config:
            variable_config = {}

        name = variable_config.get(CONF_NAME)
        value = variable_config.get(CONF_VALUE)
        attributes = variable_config.get(CONF_ATTRIBUTES)
        restore = variable_config.get(CONF_RESTORE, False)

        entities.append(Variable(variable_id, name, value, attributes, restore))

    @asyncio.coroutine
    def async_set_variable_service(call):
        """Handle calls to the set_variable service."""

        entity_id = ENTITY_ID_FORMAT.format(call.data.get(ATTR_VARIABLE))
        entity = component.get_entity(entity_id)

        if entity:
            target_variables = [ entity ]
            tasks = [variable.async_set_variable(
                        call.data.get(ATTR_VALUE),
                        call.data.get(ATTR_VALUE_TEMPLATE),
                        call.data.get(ATTR_ATTRIBUTES),
                        call.data.get(ATTR_ATTRIBUTES_TEMPLATE),
                        call.data.get(ATTR_REPLACE_ATTRIBUTES, False))
                     for variable in target_variables]
            if tasks:
                yield from asyncio.wait(tasks, loop=hass.loop)

        else:
            _LOGGER.warning('Failed to set unknown variable: %s', entity_id)

    hass.services.async_register(
        DOMAIN, SERVICE_SET_VARIABLE, async_set_variable_service,
        schema=SERVICE_SET_VARIABLE_SCHEMA)

    await component.async_add_entities(entities)
    return True

class Variable(RestoreEntity):
    """Representation of a variable."""

    def __init__(self, variable_id, name, value, attributes, restore):
        """Initialize a variable."""
        self.entity_id = ENTITY_ID_FORMAT.format(variable_id)
        self._name = name
        self._value = value
        self._attributes = attributes
        self._restore = restore

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
        if self._restore == True:
            state = await self.async_get_last_state()
            if state:
                self._value = state.state

    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return the name of the variable."""
        return self._name

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        if self._attributes is not None:
            return self._attributes.get(ATTR_ICON)
        else:
            return None

    @property
    def state(self):
        """Return the state of the component."""
        return self._value

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @asyncio.coroutine
    def async_set_variable(self, value, value_template, attributes, attributes_template, replace_attributes):
        """Update variable."""

        current_state = self.hass.states.get(self.entity_id)
        updated_attributes = None
        updated_value = None

        if not replace_attributes and self._attributes is not None:
            updated_attributes = dict(self._attributes)

        if attributes is not None:
            if updated_attributes is not None:
                updated_attributes.update(attributes)
            else:
                updated_attributes = attributes

        elif attributes_template is not None:
            attributes_template.hass = self.hass

            try:
                attributes = json.loads(attributes_template.async_render({ 'variable': current_state }))

                if isinstance(attributes, dict):
                    if updated_attributes is not None:
                        updated_attributes.update(attributes)
                    else:
                        updated_attributes = attributes

            except TemplateError as ex:
                _LOGGER.error('Could not render attribute_template %s: %s',
                    self.entity_id, ex)

        if value is not None:
            updated_value = value

        elif value_template is not None:
            try:
                value_template.hass = self.hass
                updated_value = value_template.async_render({ 'variable': current_state })
            except TemplateError as ex:
                _LOGGER.error('Could not render value_template %s: %s',
                    self.entity_id, ex)

        self._attributes = updated_attributes;

        if updated_value is not None:
            self._value = updated_value;

        yield from self.async_update_ha_state()
