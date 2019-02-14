"""
Support for GTFS (Google/General Transport Format Schema).

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.gtfs/
"""
import os
import logging
import datetime
import threading

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pygtfs==0.1.5']

_LOGGER = logging.getLogger(__name__)

CONF_DATA = 'data'
CONF_DESTINATION = 'destination'
CONF_ORIGIN = 'origin'
CONF_OFFSET = 'offset'
CONF_TOMORROW = 'include_tomorrow'

DEFAULT_NAME = 'GTFS Sensor'
DEFAULT_PATH = 'gtfs'

ICON = 'mdi:train'
ICONS = {
    0: 'mdi:tram',
    1: 'mdi:subway',
    2: 'mdi:train',
    3: 'mdi:bus',
    4: 'mdi:ferry',
    5: 'mdi:train-variant',
    6: 'mdi:gondola',
    7: 'mdi:stairs',
}

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ORIGIN): cv.string,
    vol.Required(CONF_DESTINATION): cv.string,
    vol.Required(CONF_DATA): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_OFFSET, default=0): cv.time_period,
    vol.Optional(CONF_TOMORROW, default=False): cv.boolean,
})


def get_next_departure(sched, start_station_id, end_station_id, offset,
                       include_tomorrow=False):
    """Get the next departure for the given schedule."""
    origin_station = sched.stops_by_id(start_station_id)[0]
    destination_station = sched.stops_by_id(end_station_id)[0]

    now = datetime.datetime.now() + offset
    now_date = now.strftime(DATE_FORMAT)
    yesterday = now - datetime.timedelta(days=1)
    yesterday_date = yesterday.strftime(DATE_FORMAT)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_date = tomorrow.strftime(DATE_FORMAT)

    from sqlalchemy.sql import text

    # Fetch all departures for yesterday, today and optionally tomorrow,
    # up to an overkill maximum in case of a departure every minute for those
    # days.
    limit = 24 * 60 * 60 * 2
    tomorrow_select = tomorrow_where = tomorrow_order = ''
    if include_tomorrow:
        limit = limit / 2 * 3
        tomorrow_name = tomorrow.strftime('%A').lower()
        tomorrow_select = "calendar.{} AS tomorrow,".format(tomorrow_name)
        tomorrow_where = "OR calendar.{} = 1".format(tomorrow_name)
        tomorrow_order = "calendar.{} DESC,".format(tomorrow_name)

    sql_query = """
        SELECT trip.trip_id, trip.route_id,
               time(origin_stop_time.arrival_time) AS origin_arrival_time,
               time(origin_stop_time.departure_time) AS origin_depart_time,
               date(origin_stop_time.departure_time) AS origin_departure_date,
               origin_stop_time.drop_off_type AS origin_drop_off_type,
               origin_stop_time.pickup_type AS origin_pickup_type,
               origin_stop_time.shape_dist_traveled AS origin_dist_traveled,
               origin_stop_time.stop_headsign AS origin_stop_headsign,
               origin_stop_time.stop_sequence AS origin_stop_sequence,
               time(destination_stop_time.arrival_time) AS dest_arrival_time,
               time(destination_stop_time.departure_time) AS dest_depart_time,
               destination_stop_time.drop_off_type AS dest_drop_off_type,
               destination_stop_time.pickup_type AS dest_pickup_type,
               destination_stop_time.shape_dist_traveled AS dest_dist_traveled,
               destination_stop_time.stop_headsign AS dest_stop_headsign,
               destination_stop_time.stop_sequence AS dest_stop_sequence,
               calendar.{yesterday_name} AS yesterday,
               calendar.{today_name} AS today,
               {tomorrow_select}
               calendar.start_date AS start_date,
               calendar.end_date AS end_date
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
        WHERE (calendar.{yesterday_name} = 1
               OR calendar.{today_name} = 1
               {tomorrow_where}
               )
        AND start_station.stop_id = :origin_station_id
                   AND end_station.stop_id = :end_station_id
        AND origin_stop_sequence < dest_stop_sequence
        AND calendar.start_date <= :today
        AND calendar.end_date >= :today
        ORDER BY calendar.{yesterday_name} DESC,
                 calendar.{today_name} DESC,
                 {tomorrow_order}
                 origin_stop_time.departure_time
        LIMIT :limit
        """.format(yesterday_name=yesterday.strftime('%A').lower(),
                   today_name=now.strftime('%A').lower(),
                   tomorrow_select=tomorrow_select,
                   tomorrow_where=tomorrow_where,
                   tomorrow_order=tomorrow_order)
    result = sched.engine.execute(text(sql_query),
                                  origin_station_id=origin_station.id,
                                  end_station_id=destination_station.id,
                                  today=now_date,
                                  limit=limit)

    # Create lookup timetable for today and possibly tomorrow, taking into
    # account any departures from yesterday scheduled after midnight,
    # as long as all departures are within the calendar date range.
    timetable = {}
    yesterday_first = today_first = tomorrow_first = None
    for row in result:
        row = dict(row)
        if row['yesterday'] == 1 and yesterday_date >= row['start_date']:
            row['day'] = 'yesterday'
            if yesterday_first is None:
                yesterday_first = row['origin_departure_date']
            if yesterday_first != row['origin_departure_date']:
                idx = '{} {}'.format(now_date,
                                     row['origin_depart_time'])
                timetable[idx] = row
        if row['today'] == 1:
            row['day'] = 'today'
            if today_first is None:
                today_first = row['origin_departure_date']
            if today_first == row['origin_departure_date']:
                idx_prefix = now_date
            else:
                idx_prefix = tomorrow_date
            idx = '{} {}'.format(idx_prefix, row['origin_depart_time'])
            timetable[idx] = row
        if 'tomorrow' in row and row['tomorrow'] == 1 and tomorrow_date <= \
                row['end_date']:
            row['day'] = 'tomorrow'
            if tomorrow_first is None:
                tomorrow_first = row['origin_departure_date']
            if tomorrow_first == row['origin_departure_date']:
                idx = '{} {}'.format(tomorrow_date,
                                     row['origin_depart_time'])
                timetable[idx] = row

    _LOGGER.debug("Timetable: %s", sorted(timetable.keys()))

    item = {}
    for key in sorted(timetable.keys()):
        if datetime.datetime.strptime(key, TIME_FORMAT) > now:
            item = timetable[key]
            _LOGGER.debug("Departure found for station %s @ %s -> %s",
                          start_station_id, key, item)
            break

    if item == {}:
        return None

    origin_arrival_time = '{} {}'.format(now_date, item['origin_arrival_time'])
    origin_depart_time = '{} {}'.format(now_date, item['origin_depart_time'])
    dest_arrival_time = '{} {}'.format(now_date, item['dest_arrival_time'])
    dest_depart_time = '{} {}'.format(now_date, item['dest_depart_time'])

    depart_time = datetime.datetime.strptime(origin_depart_time, TIME_FORMAT)
    arrival_time = datetime.datetime.strptime(dest_arrival_time, TIME_FORMAT)

    seconds_until = (depart_time - datetime.datetime.now()).total_seconds()
    minutes_until = int(seconds_until / 60)

    route = sched.routes_by_id(item['route_id'])[0]

    origin_stop_time_dict = {
        'Arrival Time': origin_arrival_time,
        'Departure Time': origin_depart_time,
        'Drop Off Type': item['origin_drop_off_type'],
        'Pickup Type': item['origin_pickup_type'],
        'Shape Dist Traveled': item['origin_dist_traveled'],
        'Headsign': item['origin_stop_headsign'],
        'Sequence': item['origin_stop_sequence']
    }

    destination_stop_time_dict = {
        'Arrival Time': dest_arrival_time,
        'Departure Time': dest_depart_time,
        'Drop Off Type': item['dest_drop_off_type'],
        'Pickup Type': item['dest_pickup_type'],
        'Shape Dist Traveled': item['dest_dist_traveled'],
        'Headsign': item['dest_stop_headsign'],
        'Sequence': item['dest_stop_sequence']
    }

    return {
        'trip_id': item['trip_id'],
        'day': item['day'],
        'trip': sched.trips_by_id(item['trip_id'])[0],
        'route': route,
        'agency': sched.agencies_by_id(route.agency_id)[0],
        'origin_station': origin_station,
        'departure_time': depart_time,
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
    include_tomorrow = config.get(CONF_TOMORROW)

    if not os.path.exists(gtfs_dir):
        os.makedirs(gtfs_dir)

    if not os.path.exists(os.path.join(gtfs_dir, data)):
        _LOGGER.error("The given GTFS data file/folder was not found")
        return False

    import pygtfs

    (gtfs_root, _) = os.path.splitext(data)

    sqlite_file = "{}.sqlite?check_same_thread=False".format(gtfs_root)
    joined_path = os.path.join(gtfs_dir, sqlite_file)
    gtfs = pygtfs.Schedule(joined_path)

    # pylint: disable=no-member
    if not gtfs.feeds:
        pygtfs.append_feed(gtfs, os.path.join(gtfs_dir, data))

    add_entities([
        GTFSDepartureSensor(gtfs, name, origin, destination, offset,
                            include_tomorrow)])


class GTFSDepartureSensor(Entity):
    """Implementation of an GTFS departures sensor."""

    def __init__(self, pygtfs, name, origin, destination, offset,
                 include_tomorrow):
        """Initialize the sensor."""
        self._pygtfs = pygtfs
        self.origin = origin
        self.destination = destination
        self._include_tomorrow = include_tomorrow
        self._offset = offset
        self._custom_name = name
        self._icon = ICON
        self._name = ''
        self._unit_of_measurement = 'min'
        self._state = None
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
        return self._icon

    def update(self):
        """Get the latest data from GTFS and update the states."""
        with self.lock:
            self._departure = get_next_departure(
                self._pygtfs, self.origin, self.destination, self._offset,
                self._include_tomorrow)
            if not self._departure:
                self._state = None
                self._attributes = {}
                self._attributes['Info'] = "No more departures" if \
                    self._include_tomorrow else "No more departures today"
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
            trip_id = self._departure['trip_id']

            name = '{} {} to {} next departure'
            self._name = (self._custom_name or
                          name.format(agency.agency_name,
                                      origin_station.stop_id,
                                      destination_station.stop_id))

            self._icon = ICONS.get(route.route_type, ICON)

            # Build attributes
            self._attributes['day'] = self._departure['day']
            self._attributes['offset'] = self._offset.seconds / 60

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

            if "Agency ID" not in self._attributes.keys():
                append_keys(dict_for_table(agency), 'Agency')

            if "Route ID" not in self._attributes.keys():
                append_keys(dict_for_table(route), 'Route')

            if "Origin Station Stop ID" not in self._attributes.keys():
                append_keys(dict_for_table(origin_station), "Origin Station")

            if "Destination Station Stop ID" not in self._attributes.keys():
                append_keys(dict_for_table(destination_station),
                            "Destination Station")

            if "Trip ID" not in self._attributes.keys() \
                    or self._attributes["Trip ID"] != trip_id:
                _LOGGER.info("Fetch trip details for %s", trip_id)
                append_keys(dict_for_table(trip), 'Trip')
                append_keys(origin_stop_time, "Origin Stop")
                append_keys(destination_stop_time, "Destination Stop")
