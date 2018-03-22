# Sensors

Each YAML file groups together all related sensors and contains details on usage.


## Device sensors

### [`😓 ./climate.yaml`](climate.yaml)

Indoor climate conditions.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-climate.png" alt="Climate Control group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-climate-dark.png" alt="Climate Control group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Climate Control group.</strong></p>
        </figcaption>
    </figure>
    <figure>
        <div>
            <img src="../www/screenshots/group-humidity.png" alt="Humidity group" width="325" title="Normal theme">
            <img src="../www/screenshots/group-humidity-dark.png" alt="Humidity group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Humidity group.</strong></p>
        </figcaption>
    </figure>
    <figure>
        <div>
            <img src="../www/screenshots/group-temperature.png" alt="Temperature group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-temperature-dark.png" alt="Temperature group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Temperature group.</strong></p>
        </figcaption>
    </figure>
</div>


### [`💡 ./light.yaml`](light.yaml)

Reports on loaded effects for smart lights.


### [`🔋 ./power.yaml`](power.yaml)

Battery levels.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-battery.png" alt="Battery Levels group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-battery-dark.png" alt="Battery Levels group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Battery Levels group.</strong></p>
        </figcaption>
    </figure>
</div>


## Data-source sensors

### [`🌫 ./atmosphere.yaml`](atmosphere.yaml)

[Atmospheric pollution](https://waqi.info/), UV Index and [chances of Armageddon](https://thebulletin.org/timeline).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-atmosphere-dark.png" alt="Atmospheric Safety group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Atmospheric Safety group.</strong></p>
        </figcaption>
    </figure>
</div>

### [`🚌 ./gtfs.yaml`](gtfs.yaml)

[General Transit Feed Specification](http://gtfs.org), essentially bus schedules. See also [`/gtfs/`](../gtfs) for performance tuning of this large dataset.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-transit.png" alt="Public Transit group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-transit-dark.png" alt="Public Transit group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Public Transit group with schedules for the next three departures in two directions. Yellow (warning) and red (critical) highlights are using <a href="../themes"><code>/theme/</code></a> cards defined in <a href="../customize.yaml"><code>/customize.yaml</code></a> based on how much time is left before the bus leaves. 🚌🏃</strong></p>
        </figcaption>
    </figure>
</div>


### [`🖼 ./image.yaml`](image.yaml)

Data sources for some [`/cameras`](../cameras).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-satellite-geocolour.jpg" alt="NOAA GeoColour satellite image" title="Normal theme" width="325">
            <img src="../www/screenshots/card-satellite-vapour.jpg" alt="NOAA Water Vapour satellite image" title="Normal theme" width="325">
        </div>
        <figcaption>
            <p><strong>NOAA satellite images for North-America's East Coast.</strong></p>
        </figcaption>
    </figure>
</div>


### [`📡 ./network.yaml`](network.yaml)

Internet connection speed and latency testing. 

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-network.png" alt="Network group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-network-dark.png" alt="Network group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Network group.</strong></p>
        </figcaption>
    </figure>
</div>


### [`🤓 ./system.yaml`](system.yaml)

Geeky details on HASS and its hardware status.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-system.png" alt="System group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-system-dark.png" alt="System group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>System group.</strong></p>
        </figcaption>
    </figure>
</div>


### [`🌦 ./weather.yaml`](weather.yaml)

Everything weather related.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-weather.png" alt="Today's Weather group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-weather-dark.png" alt="Today's Weather group (dark theme)" title="Dark theme" width="325">
        </div>
        <div>
            <img src="../www/screenshots/group-forecast.png" alt="Weekly Forecast group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-forecast-dark.png" alt="Weekly Forecast group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Today's weather and weekly forecast groups.</strong></p>
        </figcaption>
    </figure>
</div>


## Generic sensors

### [`⏳ ./calendar.yaml`](calendar.yaml)

Everything time related.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-calendar.png" alt="Calendar group" title="Normal theme" width="325">
            <img src="../www/screenshots/group-calendar-dark.png" alt="Calendar group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Calendar group.</strong></p>
        </figcaption>
    </figure>
</div>


### [`⁉ ./misc.yaml`](misc.yaml)

Everything else.


## Usage

Some sensors are used for information display only in [`/groups/`](../groups) and [`/appdaemon/dashboards/`](../appdaemon/dashboards), while others are also used for [`/automations/`](../automations).


## Customization

The bulk of the customization is done in [`/customize.yaml`](../customize.yaml) and some in [`/customize_glob.yaml`](../customize_glob.yaml).
