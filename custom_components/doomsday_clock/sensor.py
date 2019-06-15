"""Sensor platform for Doomsday Clock."""
import datetime
import logging
import re

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.rest.sensor import RestData
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME, CONF_ICON, CONF_UNIT_OF_MEASUREMENT,
    CONF_VALUE_TEMPLATE, STATE_UNKNOWN)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

VERSION = '2.1.0'

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'sensor'

DEFAULT_NAME = "Doomsday Clock"
DEFAULT_ICON = 'mdi:nuke'
DEFAULT_UNIT_OF_MEASUREMENT = 'min'

CONF_ATTRIBUTION = "Threat assessment by the Bulletin of the Atomic Scientists"
CONF_RESOURCE = 'https://thebulletin.org/doomsday-clock/past-announcements/'
CONF_SELECTOR = '.uabb-infobox-title'

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(hours=6)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT,
        default=DEFAULT_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
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
        _LOGGER.error("Unable to fetch URL: %s", resource)
        return False

    add_entities([
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
        self._unit_of_measurement = unit_of_measurement
        self._icon = icon
        self._value_template = value_template
        self._selector = selector
        self._sentence = None
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
            'countdown': self._sentence,
            'time': self.numberToTime(),
        }

    @property
    def sentence(self):
        return self._sentence

    def numberStringToInt(self, value):
        """Convert textual numbers into integers."""
        switcher = {
            'eight': 8,
            'five': 5,
            'four': 4,
            'nine': 9,
            'one': 1,
            'seven': 7,
            'six': 6,
            'three': 3,
            'two': 2,
            'zero': 0,
        }

        return switcher.get(value.lower(), None)

    def sentenceToNumber(self, sentence):
        """Convert Doomsday Clock string to a number of minutes to midnight."""
        pattern = (
            r"(?:(?P<integer>\d+)"
            r"|(?P<string>zero|one|two|three|four|five|six|seven|eight|nine)"
            r"(?P<andhalf>.*?half)"
            r"|(?P<half>half)) (?:minutes|a minute) to midnight"
            )
        result = re.search(pattern, sentence, re.M | re.I)

        if result is None:
            _LOGGER.error(
                "Could not find any regex pattern in sentence: %s", sentence)
            return None

        countdown = 0
        # Integer minute.
        if (result.group('integer')):
            countdown = int(result.group('integer'))
        # String minute.
        if (result.group('string')):
            countdown = self.numberStringToInt(result.group('string'))
        # Half minute.
        if (result.group('andhalf') or result.group('half')):
            countdown += 0.5

        return countdown

    def numberToTime(self):
        """Convert a number of minutes to midnight into 24h format."""
        if self._state is not STATE_UNKNOWN:
            midnight = datetime.datetime.combine(datetime.date.today() +
                datetime.timedelta(days=1), datetime.time(0, 0, 0, 0))
            minutes = self._state // 1
            seconds = (self._state - minutes) * 60
            delta = datetime.timedelta(minutes=minutes, seconds=seconds)

            return (midnight - delta).strftime('%H:%M:%S')

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the source and updates the state."""
        self.rest.update()

        from bs4 import BeautifulSoup

        # Convert HTML into parse tree.
        raw_data = BeautifulSoup(self.rest.data, 'html.parser')

        # Find the first match, which is the current Doomsday Clock value.
        try:
            sentence = raw_data.select(self._selector)[0].text.strip()
            if not sentence:
                raise ValueError('Sentence is empty')
            self._sentence = sentence
            _LOGGER.debug("Sentence found: %s", self._sentence)
        except IndexError:
            _LOGGER.error(
                "No sentence found using selector: %s. Did the design change?",
                self._selector)
            return False
        except ValueError:
            _LOGGER.error(
                "Empty sentence found using selector %s. Did the design change?"
                , self._selector)
            return False

        # Convert the Doomsday Clock string into number of minutes to midnight.
        value = self.sentenceToNumber(self._sentence)
        _LOGGER.debug("Numeric value: %s", value)

        if value is not None:
            # Optionally parse a custom template.
            if self._value_template is not None:
                self._state = \
                    self._value_template.render_with_possible_json_value(value,
                    STATE_UNKNOWN)
            else:
                self._state = value
