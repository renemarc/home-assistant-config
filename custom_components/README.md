<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **custom_components** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#-sensorgtfspy" title="GTFS"><img src="../www/screenshots/group-transit.png" alt="Public Transit group" width="140"></a>
        <a href="#-lightlightpackpy" title="Lightpack"><img src="../www/screenshots/card-lightpack.png" alt="Lightpack card" width="140"></a>
        <a href="#-display" title="Kiosk"><img src="../www/screenshots/card-kiosk.png" alt="Kiosk card" width="140"></a>
        <a href="#-sensordoomsday_clockpy" title="Doomsday Clock"><img src="../www/screenshots/card-doomsday.png" alt="Doomsday Clock card" width="140"></a>
    </div>
</figure>

<h1 align="center">Custom components, community contributions, and overrides</h1>

## Community components

### [`🌐 ./browser_mod/`](browser_mod)

Turn your browser into a controllable entity and an audio player with the [browser_mod integration by **@thomasloven**](https://github.com/thomasloven/hass-browser_mod).

### [`🎦 ./display/`](display) and [`🎦 ./fully_kiosk/`](fully_kiosk)

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

### [`💀 ./doomsday_clock/`](doomsday_clock)

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

### [`🛒 ./hacs/`](hacs)

Install and update integrations, themes, and Lovelace widgets made by the community using the [Home Assistant Community Store](https://hacs.xyz/y).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`📺 ./lightpack/`](lightpack)

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

### [`⚡ ./rpi_power/`](rpi_power)

Verifies that the host's power supply is [providing sufficient voltage](https://community.home-assistant.io/t/raspberry-pi-power-sensor-updated-2018-07-25/58155) thanks to this [Raspberry Pi power sensor by **@ludeeus**](https://github.com/custom-components/sensor.rpi_power).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`📶 ./unifigateway/`](unifigateway)

Access high level health status of UniFi Security Gateway devices via UniFi Controller thank to [this integration from **@custom-components**](https://github.com/custom-components/sensor.unifigateway).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`❓ ./variable/`](variable)

The missing link that allows storage of non-boolean values using the [Variable component by **@rogro82**](https://github.com/rogro82/hass-variables).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Overriden components

These are default Home Assistant components that were copied from the core to alter their behaviour. These changes really should be turned into appropriate [PRs](https://github.com/home-assistant/home-assistant/pulls).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


### [`🚌 ./gtfs_custom/`](gtfs_custom)

[GTFS](https://www.home-assistant.io/integrations/gtfs/) public transit schedules component:

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

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
