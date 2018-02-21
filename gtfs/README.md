# GTFS: General Transit Feed Specification

GTFS data serves to calculate public transit routes and times. The [GTFS](https://home-assistant.io/components/sensor.gtfs/) sensor indicates how to convert new feeds into a database for local queries.


## A slow sensor

While the current implementation is precise, it is also dog-slow for many reasons:
- It is build from CSV files into an SQLite database, with keys updated on every new insert. Loads of writes then!
- The build process takes up to 4 minutes on a 2015 MacBook Pro with 16GB of RAM. Wow! It's about 10 minutes on a Raspberry Pi 3 Model B with its Samsung EVO+ SD card.
- The resulting database is a huge file to open and close with each query. It contains all the transit data needed for the next few months ...most of which I don't need whatsoever.
- Indexes are there for primary keys, but not for some important columns used for joins and sorts, resulting in both slow joins and in the creation of a temporary sort table for each query. On an SD card. Ugh.

Essentially, using this sensor leads to lags and hangs in Home Assistant while the SD card is being monopolized and trashed with useless writes.


## Speed-up solutions

The way to regain speed is to add missing indexes and delete all schedule data for every stops you don't need. You'll end up with a speedy database that can handle multiple queries per second. [This thread](https://community.home-assistant.io/t/faster-gtfs-schedule-lookups/37624) discusses it.

Ideally do perform the following steps on a better machine, like a Docker build of Home Assistant on your desktop computer. Mind you, you could still use a Raspberry Pi but it will just take longer to do all those steps and it will bore you to death.

1. Build the database. Let Home Assistant complain all it wants and wait for the database to stop growing, your sign that it is ready.
1. Connect to the resulting SQLite database via the command-line and create a backup, just in case:
 ```sql
    .backup backup_full.sqlite
 ``` 
1. Then run the following commands to delete all stops data except the few that you have configured for the sensor (say, 3333, 4444 and 5555):
 ```sql
    DELETE FROM stop_times WHERE stop_id NOT IN (3333, 4444, 5555);
    DELETE FROM stops WHERE stop_id NOT IN (3333, 4444, 5555);
 ```
1. While still connected, add the missing undexes:
 ```sql
    CREATE INDEX idx_trips_service_id ON trips(service_id);
    CREATE INDEX idx_stop_times_stop_id ON stop_times(stop_id);
    CREATE INDEX idx_stop_times_trip_id ON stop_times(trip_id);
    CREATE INDEX idx_stop_times_stop_sequence ON stop_times(stop_sequence);
    CREATE INDEX idx_stop_times_departure_time ON stop_times(departure_time);
 ```
1. In my case my transit agency did not add its own agency ID to the routes, leading to faulty queries. To fix this:
  ```sql
    UPDATE routes SET agency_id = (SELECT agency_id FROM agency WHERE feed_id = 1);
  ```
1. Finally, trim the database file to remove all the empty space within.
  ```sql
    VACUUM;
  ```

Voilà! The resulting file can be copied over to the Raspberry Pi and Home Assistant restarted. Speed at last!


## Next few scheduled stop times

I use a modified GTFS sensor at [`/custom_components/sensor/gtfs.py`](../custom_components/sensor/gtfs.py) that allows for querying the next few scheduled times. I still need to do a PR for Home Assistant to submit this change. See [`/sensors/gtfs.yaml`](../sensors/gtfs.yaml).


## Customization

Customization for the GTFS sensor is done in [`/customize.yaml`](../customize.yaml). For privacy as well as for development and testing purposes any sensitive data is hidden and referenced in the non-committed [`/secrets.yaml`](../secrets-dummy.yaml) file.
