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
from homeassistant.const import CONF_MODE, CONF_NAME
from homeassistant.helpers.entity import Entity
from typing import Optional
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pygtfs==0.1.5']

_LOGGER = logging.getLogger(__name__)

CONF_CUSTOM_SQL = 'custom_sql'
CONF_DATA = 'data'
CONF_DEPARTURES = 'departures'
CONF_DESTINATION = 'destination'
CONF_ORIGIN = 'origin'
CONF_OFFSET = 'offset'
CONF_TOMORROW = 'include_tomorrow'

DEFAULT_MODE = 'countdown'
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
MODE_AUTO = 'auto'
MODE_COUNTDOWN = 'countdown'
MODE_DEPARTURE = 'departure'
MODE_TIMER = 'timer'
MODE_TYPES = {
    MODE_AUTO,
    MODE_COUNTDOWN,
    MODE_DEPARTURE,
    MODE_TIMER,
}
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
UNIT_OF_MEASUREMENT = 'min'
DATA_KEY = 'gtfs'
NAME_FORMAT = 'GTFS {origin} to {destination}'
LOCK_KEY_FORMAT = 'lock.{source}'
TRIP_KEY_FORMAT = '{origin}::{destination}'
SQL_RESULT_PER_DAY = 1440

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ORIGIN): cv.string,
    vol.Required(CONF_DESTINATION): cv.string,
    vol.Required(CONF_DATA): cv.string,
    vol.Optional(CONF_DEPARTURES, default=0):
        vol.All(cv.ensure_list, [vol.Range(min=0, max=20)]),
    vol.Optional(CONF_MODE, default=DEFAULT_MODE): vol.In(MODE_TYPES),
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_OFFSET, default=0): cv.time_period,
    vol.Optional(CONF_TOMORROW, default=False): cv.boolean,
    vol.Optional(CONF_CUSTOM_SQL):
        vol.All(cv.ensure_list),
})


def get_next_departure(sched, start_station_id, end_station_id,
                                   offset, position, hass,
                                   include_tomorrow=False) -> Optional[dict]:
    """Get the next departure for the given schedule."""
    try:
        origin_station = sched.stops_by_id(start_station_id)[0]
        destination_station = sched.stops_by_id(end_station_id)[0]
    except IndexError:
        return None

    now = datetime.datetime.now() + offset
    # now = datetime.datetime.strptime("2019-02-14 23:45:00", TIME_FORMAT)
    now_date = now.strftime(DATE_FORMAT)
    trip_key = TRIP_KEY_FORMAT.format(origin=start_station_id,
                                      destination=end_station_id)

    # Load timetable from cache or fetch a new one.
    if trip_key in hass.data[DATA_KEY] \
            and now_date in hass.data[DATA_KEY][trip_key]['timetable']:
        timetable = hass.data[DATA_KEY][trip_key]['timetable'][now_date]
        timetable_updated = False
    else:
        _LOGGER.info("Refreshing timetable cache for %s.", now_date)

        from sqlalchemy.sql import text
        # import time
        # time.sleep(5)

        # Fetch all departures for yesterday, today and optionally tomorrow,
        # up to an overkill maximum in case of a departure every minute for
        # those days.
        yesterday = now - datetime.timedelta(days=1)
        yesterday_date = yesterday.strftime(DATE_FORMAT)
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow_date = tomorrow.strftime(DATE_FORMAT)

        limit = SQL_RESULT_PER_DAY * 2
        tomorrow_select = tomorrow_where = tomorrow_order = ''
        if include_tomorrow:
            limit = SQL_RESULT_PER_DAY * 3
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
                   {tomorrow_where})
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
            if row['yesterday'] == 1 and yesterday_date >= row['start_date']:
                if yesterday_first is None:
                    yesterday_first = row['origin_departure_date']
                if yesterday_first != row['origin_departure_date']:
                    day = {
                        'day': 'yesterday',
                        'origin_departure_date': now_date,
                    }
                    idx = '{} {}'.format(now_date,
                                         row['origin_depart_time'])
                    timetable[idx] = {**row, **day}
            if row['today'] == 1:
                if today_first is None:
                    today_first = row['origin_departure_date']
                if today_first == row['origin_departure_date']:
                    idx_prefix = now_date
                else:
                    idx_prefix = tomorrow_date
                day = {
                    'day': 'today',
                    'origin_departure_date': idx_prefix,
                }
                idx = '{} {}'.format(idx_prefix, row['origin_depart_time'])
                timetable[idx] = {**row, **day}
            if 'tomorrow' in row and row['tomorrow'] == 1 \
                    and tomorrow_date <= row['end_date']:
                if tomorrow_first is None:
                    tomorrow_first = row['origin_departure_date']
                if tomorrow_first == row['origin_departure_date']:
                    day = {
                        'day': 'tomorrow',
                        'origin_departure_date': tomorrow_date,
                    }
                    idx = '{} {}'.format(tomorrow_date,
                                         row['origin_depart_time'])
                    timetable[idx] = {**row, **day}
        timetable_updated = True

    # Find the next departure in timetable and trim the cache size if possible
    item = {}
    skip = next_day = 0
    for key in sorted(timetable.keys()):
        # Trim past departures
        if datetime.datetime.strptime(key, TIME_FORMAT) <= now:
            del timetable[key]
            timetable_updated = True
            continue

        if skip == position:
            item = timetable[key]
        skip += 1

        # Trim tomorrow's useless departures, if any
        if datetime.datetime.strptime(key, TIME_FORMAT).strftime(
                DATE_FORMAT) != now_date:
            if next_day > hass.data[DATA_KEY][trip_key]['max']:
                del timetable[key]
                timetable_updated = True
            next_day += 1

    # Update cache
    hass.data[DATA_KEY][trip_key]['timetable'] = {now_date: timetable}
    if timetable_updated:
        _LOGGER.debug("Updated timetable: %s", sorted(timetable.keys()))

    if item == {}:
        return None

    _LOGGER.debug("Departure #%d found for station %s @ %s -> %s",
                  position, start_station_id, item['origin_depart_time'], item)

    # Format arrival and departure dates and times, accounting for the
    # possibility of times crossing over midnight.
    item_date = datetime.datetime.strptime(item['origin_departure_date'],
                                           DATE_FORMAT)
    origin_depart_time = '{} {}'.format(item_date.strftime(DATE_FORMAT),
                                        item['origin_depart_time'])

    origin_arrival = item_date
    if item['origin_depart_time'] < item['origin_arrival_time']:
        origin_arrival -= datetime.timedelta(days=1)
    origin_arrival_time = '{} {}'.format(origin_arrival.strftime(DATE_FORMAT),
                                         item['origin_arrival_time'])

    dest_arrival = item_date
    if item['dest_arrival_time'] < item['origin_depart_time']:
        dest_arrival += datetime.timedelta(days=1)
    dest_arrival_time = '{} {}'.format(dest_arrival.strftime(DATE_FORMAT),
                                       item['dest_arrival_time'])

    dest_depart = dest_arrival
    if item['dest_depart_time'] < item['dest_arrival_time']:
        dest_depart += datetime.timedelta(days=1)
    dest_depart_time = '{} {}'.format(dest_depart.strftime(DATE_FORMAT),
                                      item['dest_depart_time'])

    depart_time = datetime.datetime.strptime(origin_depart_time, TIME_FORMAT)
    arrival_time = datetime.datetime.strptime(dest_arrival_time, TIME_FORMAT)

    seconds_until = (depart_time - datetime.datetime.now()).total_seconds()
    # seconds_until = (depart_time - datetime.datetime.strptime("2019-02-14 23:45:00", TIME_FORMAT)).total_seconds()
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

    try:
        agency = sched.agencies_by_id(route.agency_id)[0]
    except IndexError:
        agency = None

    return {
        'trip_id': item['trip_id'],
        'day': item['day'],
        'trip': sched.trips_by_id(item['trip_id'])[0],
        'route': route,
        'agency': agency,
        'origin_station': origin_station,
        'departure_time': depart_time,
        'destination_station': destination_station,
        'arrival_time': arrival_time,
        'seconds_until_departure': seconds_until,
        'minutes_until_departure': minutes_until,
        'origin_stop_time': origin_stop_time_dict,
        'destination_stop_time': destination_stop_time_dict
    }


def setup_platform(hass, config, add_entities, discovery_info=None) -> None:
    """Set up the GTFS sensor."""
    gtfs_dir = hass.config.path(DEFAULT_PATH)
    data = config.get(CONF_DATA)
    origin = config.get(CONF_ORIGIN)
    destination = config.get(CONF_DESTINATION)
    departures = config.get(CONF_DEPARTURES)
    mode = config.get(CONF_MODE)
    name = config.get(CONF_NAME)
    offset = config.get(CONF_OFFSET)
    include_tomorrow = config.get(CONF_TOMORROW)
    custom_sql = config.get(CONF_CUSTOM_SQL)

    if DATA_KEY not in hass.data:
        hass.data[DATA_KEY] = dict()

    lock_key = LOCK_KEY_FORMAT.format(source=data)
    trip_key = TRIP_KEY_FORMAT.format(origin=origin,
                                      destination=destination)

    hass.data[DATA_KEY][trip_key] = {
        'min': min(departures),
        'max': max(departures),
        'timetable': [],
    }

    if not os.path.exists(gtfs_dir):
        os.makedirs(gtfs_dir)

    if not os.path.exists(os.path.join(gtfs_dir, data)):
        _LOGGER.error("The given GTFS data file/folder was not found")
        return False

    import pygtfs

    (gtfs_root, _) = os.path.splitext(data)

    sqlite_file = "{}.sqlite".format(gtfs_root)
    joined_path = os.path.join(gtfs_dir, sqlite_file)

    # Reduce chances for race conditions when creating the database
    if not os.path.isfile(joined_path):
        import time
        import random
        time.sleep(random.randrange(10, 1000) / 1000)

    joined_path = "{}?check_same_thread=False".format(joined_path)
    gtfs = pygtfs.Schedule(joined_path)

    # Create database file if it doesn't exist
    # pylint: disable=no-member
    if not gtfs.feeds and lock_key not in hass.data[DATA_KEY]:
        hass.data[DATA_KEY][lock_key] = True
        _LOGGER.info("Creating database for \"%s\", this may take some time.",
                     data)
        pygtfs.append_feed(gtfs, os.path.join(gtfs_dir, data))

        import sqlalchemy

        # Run any custom SQL queries
        for sql_query in custom_sql:
            gtfs.engine.execute(sqlalchemy.sql.text(sql_query))

        # Create additional indexes to speed-up lookups
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=gtfs.engine)
        sqlalchemy.Index('ix_trips_service_id', meta.tables[
            'trips'].columns.get('service_id')).create(bind=gtfs.engine)
        sqlalchemy.Index('ix_stop_times_trip_id', meta.tables[
            'stop_times'].columns.get('trip_id')).create(bind=gtfs.engine)
        sqlalchemy.Index('ix_stop_times_stop_id', meta.tables[
            'stop_times'].columns.get('stop_id')).create(bind=gtfs.engine)
        sqlalchemy.Index('ix_stop_times_stop_sequence', meta.tables[
            'stop_times'].columns.get('stop_sequence')).create(
            bind=gtfs.engine)

        _LOGGER.info("Database \"%s.sqlite\" creation complete.", data)

    sensors = []
    for position in departures:
        sensors.append(GTFSDepartureSensor(pygtfs=gtfs,
                                           name=name, 
                                           origin=origin,
                                           destination=destination,
                                           offset=offset,
                                           position=position,
                                           mode=mode,
                                           include_tomorrow=include_tomorrow))
    add_entities(sensors, True)


class GTFSDepartureSensor(Entity):
    """Implementation of an GTFS departures sensor."""

    def __init__(self, pygtfs, name, origin, destination, offset, position,
                 include_tomorrow, mode) -> None:
        """Initialize the sensor."""
        self._pygtfs = pygtfs
        self.origin = origin
        self.destination = destination
        self.position = position
        self._departure = None
        self._include_tomorrow = include_tomorrow
        self._offset = offset
        self._icon = ICON
        self._mode = mode
        self._name = name
        self._unit_of_measurement = None
        self._state = None
        self._attributes = {}
        self.lock = threading.Lock()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        if not self._name:
            self._name = NAME_FORMAT.format(origin=self.origin,
                                            destination=self.destination)
        if self.position == 0:
            return self._name
        return '{} {} '.format(self._name, self.position)

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self) -> str:
        """Icon to use in the frontend, if any."""
        return self._icon

    def update(self) -> None:
        """Get the latest data from GTFS and update the states."""
        with self.lock:
            self._departure = get_next_departure(
                self._pygtfs, self.origin, self.destination, self._offset,
                self.position, self.hass, self._include_tomorrow)
            if not self._departure:
                self._state = None
                self._attributes = dict()
                self._attributes['Info'] = "No more departures" if \
                    self._include_tomorrow else "No more departures today"
                return

            minutes = self._departure['minutes_until_departure']
            origin_station = self._departure['origin_station']
            destination_station = self._departure['destination_station']
            origin_stop_time = self._departure['origin_stop_time']
            destination_stop_time = self._departure['destination_stop_time']
            agency = self._departure['agency']
            route = self._departure['route']
            trip = self._departure['trip']
            trip_id = self._departure['trip_id']

            if self._mode == MODE_DEPARTURE:
                self._state = datetime.datetime.strptime(
                    origin_stop_time["Departure Time"],
                    TIME_FORMAT).strftime('%H:%M')
                self._unit_of_measurement = None
            elif self._mode == MODE_TIMER or self._mode == MODE_AUTO and \
                    abs(minutes) >= 60:
                hour = int(minutes / 60)
                minute = abs(minutes) % 60
                self._state = '{0}:{1:02d}'.format(hour, minute)
                self._unit_of_measurement = None
            else:
                self._state = minutes
                self._unit_of_measurement = UNIT_OF_MEASUREMENT

            self._icon = ICONS.get(route.route_type, ICON)

            # Build attributes
            self._attributes['day'] = self._departure['day']
            self._attributes['offset'] = self._offset.seconds / 60

            def dict_for_table(resource) -> dict:
                """Return a dict for the SQLAlchemy resource given."""
                return dict((col, getattr(resource, col))
                            for col in resource.__table__.columns.keys())

            def append_keys(resource, prefix=None) -> None:
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

            if "Agency ID" not in self._attributes.keys() and agency:
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
