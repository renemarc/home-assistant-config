<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **custom_components** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#-sensorgtfspy" title="GTFS"><img src="../www/screenshots/group-transit.png" alt="Public Transit group" width="140"></a>
        <a href="#-lightlightpackpy" title="Lightpack"><img src="../www/screenshots/card-lightpack.png" alt="Lightpack card" width="140"></a>
        <a href="#-display" title="Kiosk"><img src="../www/screenshots/card-kiosk.png" alt="Kiosk card" width="140"></a>
        <a href="#-sensordoomsday_clockpy" title="Doomsday Clock"><img src="../www/screenshots/card-doomsday.png" alt="Doomsday Clock card" width="140"></a>
        <a href="#-sensorwaqipy" title="WAQI"><img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Atmospheric Safety group" width="140"></a>
    </div>
</figure>

<h1 align="center">Custom components, community contributions, and overrides</h1>

## Community components

### [`🎦 ./display/`](display)

Interact with Android devices running the [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser) thanks to the [Display platform by **@daemondazz**](https://github.com/daemondazz/homeassistant-displays).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-kiosk.png" alt="Kiosk card" title="Kiosk control" width="325">
        </div>
        <figcaption>
            <p><strong>Kiosk control.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`📺 ./lightpack/light.py`](lightpack/light.py)

Supports basic operation of [Prismatik](https://github.com/psieg/Lightpack) monitor bias lighting using this [Lightpack component by **@kklemm91**](https://github.com/kklemm91/Lightpack-HASS).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-lightpack.png" alt="Lightpack card" title="Lightpack control" width="325">
        </div>
        <figcaption>
            <p><strong>Lightpack control.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`💀 ./doomsday_clock/sensor.py`](doomsday_clock/sensor.py)

A local copy of my depressing [Doomsday Clock sensor](https://github.com/renemarc/home-assistant-doomsday-clock) that tracks the _Bulletin of the Atomic Scientists_' [world threat assessment index](https://thebulletin.org/doomsday-clock/) indicating how close humanity is to a man-made global catastrophe either through nuclear war or climate change.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-doomsday.png" alt="Doomsday Clock card" title="Doomsday Clock" width="325">
        </div>
        <figcaption>
            <p><strong>Doomsday Clock.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⚡ ./rpi_power/sensor.py`](rpi_power/sensor.py)

Verifies that the host's power supply is [providing sufficient voltage](https://community.home-assistant.io/t/raspberry-pi-power-sensor-updated-2018-07-25/58155) thanks to this [Raspberry Pi power sensor by **@ludeeus**](https://github.com/custom-components/sensor.rpi_power).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`❓ ./variable.py`](variables.py)

The missing link that allows storage of non-boolean values using the [Variable component by **@rogro82**](https://github.com/rogro82/hass-variables).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Overriden components

These are default Home Assistant components that were copied from the core to alter their behaviour. These changes really should be turned into appropriate [PRs](https://github.com/home-assistant/home-assistant/pulls).

### [`🚌 ./sensor/gtfs.py`](sensor/gtfs.py)

[GTFS](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/gtfs.py) public transit schedules component:

- Added support for next bus departures.
- Simplified query, making it cacheable in order to increase IO performance.
- Allow querying departures after midnight.
- Correctly set arrival date to tommorow when bus leaves before midnight but arrives after.
- Return **Null** instead of **Zero** when a departure is not found/available.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-transit.png" alt="Public Transit group" title="Public Transit" width="325">
        </div>
        <figcaption>
            <p><strong>Public Transit group with schedules for the next three departures in two directions. Got to catch that bus! 🚌🏃</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🌫 ./sensor/waqi.py`](sensor/waqi.py)

[WAQI](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/waqi.py) World Air Quality Index:

- Added support for location query by UID (otherwise some locations are never returned when doing a general keyword search).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Atmospheric Safety group" width="325">
        </div>
        <figcaption>
            <p><strong>World Air Quality Index</strong></p>
        </figcaption>
    </figure>
</div>

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
