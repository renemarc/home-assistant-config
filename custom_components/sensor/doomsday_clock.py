"""
Support for Doomsday Clock from the Bulletin of the Atomic Scientists.

Convert data into parsable time from the Timeline page at
https://thebulletin.org/timeline

Based on work by Matt Bierner.
See https://github.com/mattbierner/MinutesToMidnight

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.doomsday_clock/
"""
import logging
import re
import voluptuous as vol
from datetime import timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor.rest import RestData
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_ICON, CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['beautifulsoup4==4.6.0']

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Doomsday Clock'
DEFAULT_ICON = 'mdi:nuke'
DEFAULT_UNIT_OF_MEASUREMENT = 'min'

CONF_ATTRIBUTION = "Bulletin of the Atomic Scientists"
CONF_RESOURCE = 'https://thebulletin.org/timeline'
CONF_SELECTOR = '#content .view-content .node-title'

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT,
        default=DEFAULT_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Doomsday Clock sensor."""
    name = config.get(CONF_NAME)
    resource = CONF_RESOURCE
    method = 'GET'
    selector = CONF_SELECTOR
    payload = headers = auth = None
    verify_ssl = False
    unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)
    icon = config.get(CONF_ICON)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
        value_template.hass = hass

    rest = RestData(method, resource, auth, headers, payload, verify_ssl)
    rest.update()

    if rest.data is None:
        _LOGGER.error("Unable to fetch data from %s", resource)
        return False

    add_devices([
        DoomsdayClockSensor(rest, name, selector, unit_of_measurement, icon,
            value_template)
        ], True)


class DoomsdayClockSensor(Entity):
    """Representation of a Doomsday Clock sensor."""

    def __init__(self, rest, name, selector, unit_of_measurement, icon,
        value_template):
        """Initialize a Doomsday Clock sensor."""
        self.rest = rest
        self._name = name
        self._state = STATE_UNKNOWN
        self._unit_of_measurement = unit_of_measurement
        self._icon = icon
        self._value_template = value_template
        self._selector = selector
        self._sentence = None

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
        return self._unit_of_measurement

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
            "minutes_to_midnight": self._sentence,
        }

    @property
    def sentence(self):
        return self._sentence

    def numberStringToInt(self, value):
        switcher = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        return switcher.get(value.lower(), None)

    def sentenceToNumber(self, sentence):
        pattern = (
            r'(?:(?P<integer>\d+)'
            r'|(?P<string>zero|one|two|three|four|five|six|seven|eight|nine)'
            r'(?P<andhalf>.*?half)'
            r'|(?P<half>half)) (?:minutes|a minute) to midnight'
            )
        result = re.search(pattern, sentence, re.M | re.I)

        if result:
            countdown = 0
            # Integer minute
            if (result.group('integer')):
                countdown = int(result.group('integer'))
            # String minute
            if (result.group('string')):
                countdown = self.numberStringToInt(result.group('string'))
            # Half minute
            if (result.group('andhalf') or result.group('half')):
                countdown += 0.5

            return countdown
        else:
            _LOGGER.error(
                'Could not find pattern "%s" in sentence "%s"', pattern,
                sentence)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the source and updates the state."""
        self.rest.update()

        from bs4 import BeautifulSoup

        raw_data = BeautifulSoup(self.rest.data, 'html.parser')
        _LOGGER.debug(raw_data)

        self._sentence = raw_data.select(self._selector)[0].text.strip()
        _LOGGER.debug(self._sentence)

        value = self.sentenceToNumber(self._sentence)
        _LOGGER.debug(value)

        if self._value_template is not None:
            self._state = self._value_template.render_with_possible_json_value(
                value, STATE_UNKNOWN)
        else:
            self._state = value
