"""Sensor platform for Doomsday Clock."""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_SECONDS,
    ATTR_TIME,
    CONF_ICON,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE,
    STATE_UNKNOWN,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

VERSION = '2.2.0'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'sensor'

DEFAULT_NAME = 'Doomsday Clock'
DEFAULT_ICON = 'mdi:nuke'

UNIT_MINUTES = 'min'
UNIT_SECONDS = 's'

MINUTE_FRACTIONS = (0, 30)

CONF_ATTRIBUTION = 'Threat assessment by the Bulletin of the Atomic Scientists'
ATTR_CLOCK = 'clock'
ATTR_MINUTES = 'minutes'
ATTR_SENTENCE = 'countdown'

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=6)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None) -> None:
    """Set up the Doomsday Clock sensor."""
    from countdoom import CountdoomClient

    name = config.get(CONF_NAME)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
        value_template.hass = hass
    _LOGGER.debug('async_setup_platform()')

    device = DoomsdayClockSensor(
        hass=hass,
        client=CountdoomClient(),
        name=name,
        unit=config.get(CONF_UNIT_OF_MEASUREMENT),
        icon=config.get(CONF_ICON),
        value_template=value_template,
    )
    async_add_entities([device], update_before_add=True)


class DoomsdayClockSensor(Entity):
    """Representation of a Doomsday Clock sensor."""

    def __init__(self, hass, client, name, unit, icon, value_template):
        """Initialize a Doomsday Clock sensor."""
        self.hass = hass
        self._client = client
        self._name = name
        self._unit = None
        self.custom_unit = unit
        self._icon = icon
        self._value_template = value_template
        self._sentence = None
        self._clock = None
        self._time = None
        self._minutes = None
        self._seconds = None
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit_of_measurement of the sensor."""
        return self._unit

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
            ATTR_SENTENCE: self.sentence,
            ATTR_TIME: self.time,
            ATTR_CLOCK: self.clock,
            ATTR_MINUTES: self.minutes,
            ATTR_SECONDS: self.seconds,
        }

    @property
    def sentence(self):
        return self._sentence

    @property
    def clock(self):
        return self._clock

    @property
    def time(self):
        return self._time

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return self._seconds

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Get the latest data from the source and updates the state."""

        _LOGGER.debug('async_update()')
        data = await self._client.fetch_data()
        if data is None:
            _LOGGER.warning('Countdoom Client returned an empty data set.')
            return
        _LOGGER.debug('Received data set: %s', data)

        state = data.get('countdown')
        self._seconds = state
        self._sentence = data.get('sentence')
        self._clock = data.get('clock')
        self._time = data.get('time')
        self._minutes = data.get('minutes')

        # Optionally parse a custom template.
        if self._value_template is not None:
            self._state = \
                self._value_template.render_with_possible_json_value(
                    state,
                    STATE_UNKNOWN
                )
            return

        # Set the proper unit of measure.
        if self.custom_unit is not None:
            self._unit = self.custom_unit
        elif state >= 60 and state % 60 in MINUTE_FRACTIONS:
            self._unit = UNIT_MINUTES
        else:
            self._unit = UNIT_SECONDS

        # Convert seconds to minutes, if relevant..
        if state >= 60 and state % 60 in MINUTE_FRACTIONS:
            state = round(state / 60, 2)
        if state.is_integer():
            state = int(state)
        self._state = state
