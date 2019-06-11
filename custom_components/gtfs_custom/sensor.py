"""Support for GTFS (Google/General Transport Format Schema)."""
import os
import logging
import datetime
import threading

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_DATA = 'data'
CONF_DESTINATION = 'destination'
CONF_ORIGIN = 'origin'
CONF_OFFSET = 'offset'
CONF_POSITION = 'position'

DEFAULT_NAME = 'GTFS Sensor'
DEFAULT_PATH = 'gtfs'
DEFAULT_POSITION = '1'

ICON = 'mdi:train'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ORIGIN): cv.string,
    vol.Required(CONF_DESTINATION): cv.string,
    vol.Required(CONF_DATA): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_OFFSET, default=0): cv.time_period,
    vol.Optional(CONF_POSITION, default=DEFAULT_POSITION): cv.positive_int,
})


def get_next_departure(sched, start_station_id, end_station_id, offset,
    position):
    """Get the next departure for the given schedule."""
    origin_station = sched.stops_by_id(start_station_id)[0]
    destination_station = sched.stops_by_id(end_station_id)[0]

    now = datetime.datetime.now() + offset
    day_name = now.strftime('%A').lower()
    now_str = now.strftime('%H:%M:%S')
    now_time = now.time()
    today = now.strftime('%Y-%m-%d')
    tomorrow_obj = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow = tomorrow_obj.strftime('%Y-%m-%d')
    skip = int(position) - 1

    from sqlalchemy.sql import text

    sql_query = text("""
    SELECT trip.trip_id, trip.route_id,
           time(origin_stop_time.departure_time),
           time(destination_stop_time.arrival_time),
           time(origin_stop_time.arrival_time),
           time(origin_stop_time.departure_time),
           origin_stop_time.drop_off_type,
           origin_stop_time.pickup_type,
           origin_stop_time.shape_dist_traveled,
           origin_stop_time.stop_headsign,
           origin_stop_time.stop_sequence,
           time(destination_stop_time.arrival_time),
           time(destination_stop_time.departure_time),
           destination_stop_time.drop_off_type,
           destination_stop_time.pickup_type,
           destination_stop_time.shape_dist_traveled,
           destination_stop_time.stop_headsign,
           destination_stop_time.stop_sequence
    FROM trips trip
    INNER JOIN calendar calendar
               ON trip.service_id = calendar.service_id
    INNER JOIN stop_times origin_stop_time
               ON trip.trip_id = origin_stop_time.trip_id
    INNER JOIN stops start_station
               ON origin_stop_time.stop_id = start_station.stop_id
    INNER JOIN stop_times destination_stop_time
               ON trip.trip_id = destination_stop_time.trip_id
    INNER JOIN stops end_station
               ON destination_stop_time.stop_id = end_station.stop_id
    WHERE calendar.{day_name} = 1
    AND start_station.stop_id = :origin_station_id
    AND end_station.stop_id = :end_station_id
    AND origin_stop_time.stop_sequence < destination_stop_time.stop_sequence
    AND calendar.start_date <= :today
    AND calendar.end_date >= :today
    ORDER BY origin_stop_time.departure_time
    """.format(day_name=day_name))
    result = sched.engine.execute(sql_query,
                                  origin_station_id=origin_station.id,
                                  end_station_id=destination_station.id,
                                  today=today)

    rows = result.fetchall()
    item = {}
    for i,row in enumerate(rows):
        if (datetime.datetime.strptime(row[2], '%H:%M:%S').time() > now_time):
            schedule_idx = i + skip
            if schedule_idx < len(rows):
                item = rows[schedule_idx]
                if (datetime.datetime.strptime(item[2], '%H:%M:%S').time()
                    <= now_time):
                    today = tomorrow
            break

    if item == {}:
        return None

    departure_time_string = '{} {}'.format(today, item[2])
    arrival_time_string = '{} {}'.format(today if item[3] > item[2]
                                         else tomorrow, item[3])
    departure_time = datetime.datetime.strptime(departure_time_string,
                                                TIME_FORMAT)
    arrival_time = datetime.datetime.strptime(arrival_time_string,
                                              TIME_FORMAT)

    seconds_until = (departure_time-datetime.datetime.now()).total_seconds()
    minutes_until = int(seconds_until / 60)

    route = sched.routes_by_id(item[1])[0]

    origin_stoptime_arrival_time = '{} {}'.format(today, item[4])
    origin_stoptime_departure_time = '{} {}'.format(today, item[5])
    dest_stoptime_arrival_time = '{} {}'.format(today if item[11] > item[5]
                                                else tomorrow, item[11])
    dest_stoptime_depart_time = '{} {}'.format(today if item[12] > item[5]
                                               else tomorrow, item[12])

    origin_stop_time_dict = {
        'Arrival Time': origin_stoptime_arrival_time,
        'Departure Time': origin_stoptime_departure_time,
        'Drop Off Type': item[6], 'Pickup Type': item[7],
        'Shape Dist Traveled': item[8], 'Headsign': item[9],
        'Sequence': item[10]
    }

    destination_stop_time_dict = {
        'Arrival Time': dest_stoptime_arrival_time,
        'Departure Time': dest_stoptime_depart_time,
        'Drop Off Type': item[13], 'Pickup Type': item[14],
        'Shape Dist Traveled': item[15], 'Headsign': item[16],
        'Sequence': item[17]
    }

    return {
        'trip_id': item[0],
        'trip': sched.trips_by_id(item[0])[0],
        'route': route,
        'agency': sched.agencies_by_id(route.agency_id)[0],
        'origin_station': origin_station,
        'departure_time': departure_time,
        'destination_station': destination_station,
        'arrival_time': arrival_time,
        'seconds_until_departure': seconds_until,
        'minutes_until_departure': minutes_until,
        'origin_stop_time': origin_stop_time_dict,
        'destination_stop_time': destination_stop_time_dict
    }


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the GTFS sensor."""
    gtfs_dir = hass.config.path(DEFAULT_PATH)
    data = config.get(CONF_DATA)
    origin = config.get(CONF_ORIGIN)
    destination = config.get(CONF_DESTINATION)
    name = config.get(CONF_NAME)
    offset = config.get(CONF_OFFSET)
    position = config.get(CONF_POSITION)

    if not os.path.exists(gtfs_dir):
        os.makedirs(gtfs_dir)

    if not os.path.exists(os.path.join(gtfs_dir, data)):
        _LOGGER.error("The given GTFS data file/folder was not found")
        return False

    import pygtfs

    split_file_name = os.path.splitext(data)

    sqlite_file = "{}.sqlite".format(split_file_name[0])
    joined_path = os.path.join(gtfs_dir, sqlite_file)
    gtfs = pygtfs.Schedule(joined_path)

    # pylint: disable=no-member
    if not gtfs.feeds:
        pygtfs.append_feed(gtfs, os.path.join(gtfs_dir, data))

    add_entities([
        GTFSDepartureSensor(gtfs, name, origin, destination, offset,
            position)])


class GTFSDepartureSensor(Entity):
    """Implementation of an GTFS departures sensor."""

    def __init__(self, pygtfs, name, origin, destination, offset, position):
        """Initialize the sensor."""
        self._pygtfs = pygtfs
        self.origin = origin
        self.destination = destination
        self._offset = offset
        self._position = position
        self._custom_name = name
        self._name = ''
        self._unit_of_measurement = 'min'
        self._state = 0
        self._attributes = {}
        self.lock = threading.Lock()
        self.update()

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
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    def update(self):
        """Get the latest data from GTFS and update the states."""
        with self.lock:
            self._departure = get_next_departure(
                self._pygtfs, self.origin, self.destination, self._offset,
                self._position)
            if not self._departure:
                self._state = None
                self._attributes = {
                    'position': self._position,
                    'Info': 'No more departures today',
                    }
                if self._name == '':
                    self._name = (self._custom_name or DEFAULT_NAME)
                return

            self._state = self._departure['minutes_until_departure']

            origin_station = self._departure['origin_station']
            destination_station = self._departure['destination_station']
            origin_stop_time = self._departure['origin_stop_time']
            destination_stop_time = self._departure['destination_stop_time']
            agency = self._departure['agency']
            route = self._departure['route']
            trip = self._departure['trip']

            name = '{} {} to {} next departure'
            self._name = (self._custom_name or
                          name.format(agency.agency_name,
                                      origin_station.stop_id,
                                      destination_station.stop_id))

            # Build attributes
            self._attributes = {}
            self._attributes['offset'] = self._offset.seconds / 60
            self._attributes['position'] = self._position

            def dict_for_table(resource):
                """Return a dict for the SQLAlchemy resource given."""
                return dict((col, getattr(resource, col))
                            for col in resource.__table__.columns.keys())

            def append_keys(resource, prefix=None):
                """Properly format key val pairs to append to attributes."""
                for key, val in resource.items():
                    if val == "" or val is None or key == 'feed_id':
                        continue
                    pretty_key = key.replace('_', ' ')
                    pretty_key = pretty_key.title()
                    pretty_key = pretty_key.replace('Id', 'ID')
                    pretty_key = pretty_key.replace('Url', 'URL')
                    if prefix is not None and \
                       pretty_key.startswith(prefix) is False:
                        pretty_key = '{} {}'.format(prefix, pretty_key)
                    self._attributes[pretty_key] = val

            append_keys(dict_for_table(agency), 'Agency')
            append_keys(dict_for_table(route), 'Route')
            append_keys(dict_for_table(trip), 'Trip')
            append_keys(dict_for_table(origin_station), 'Origin Station')
            append_keys(dict_for_table(destination_station),
                        'Destination Station')
            append_keys(origin_stop_time, 'Origin Stop')
            append_keys(destination_stop_time, 'Destination Stop')
