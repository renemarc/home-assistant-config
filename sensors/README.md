<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **sensors** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#-climateyaml" title="Climate"><img src="../www/screenshots/group-climate.png" alt="Climate Control group" width="140"></a>
        <a href="#-poweryaml" title="Power"><img src="../www/screenshots/group-battery.png" alt="Battery Levels group" width="140"></a>
        <a href="#-atmosphereyaml" title="Atmosphere"><img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" width="140"></a>
        <a href="#-gtfsyaml" title="Public Transit"><img src="../www/screenshots/group-transit.png" alt="Public Transit group" width="140"></a>
    </div>
    <div align="center">
        <a href="#-networkyaml" title="Network"><img src="../www/screenshots/group-network.png" alt="Network group" width="140"></a>
        <a href="#-systemyaml" title="System"><img src="../www/screenshots/group-system.png" alt="System group" width="140"></a>
        <a href="#-weatheryaml" title="Weather"><img src="../www/screenshots/group-weather.png" alt="Today's Weather group" width="140"></a>
        <a href="#-calendaryaml" title="Calendar"><img src="../www/screenshots/group-calendar.png" alt="Calendar group" width="140"></a>
        <a href="#-camerayaml" title="Cameras"><img src="../www/screenshots/card-satellite-geocolour.jpg" alt="NOAA GeoColour satellite image" width="140"></a>
    </div>
</figure>

<h1 align="center">Sensors</h1>

Each YAML file groups together all related sensors and contains details on usage.

## Device sensors

### [`😓 ./climate.yaml`](climate.yaml)

Indoor climate conditions and air quality.

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`💡 ./light.yaml`](light.yaml)

Reports on loaded effects for smart lights.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🔋 ./power.yaml`](power.yaml)

Battery levels and power monitoring.

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`📸 ./camera.yaml`](camera.yaml)

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⁉ ./misc.yaml`](misc.yaml)

Everything else, including printer consumables status.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Usage

Some sensors are used for information display only in [`/groups/`](../groups) and [`/appdaemon/dashboards/`](../appdaemon/dashboards), while others are also used for [`/automations/`](../automations).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Customization

The bulk of the customization is done in [`/customize.yaml`](../customize.yaml) and some in [`/customize_glob.yaml`](../customize_glob.yaml).

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
