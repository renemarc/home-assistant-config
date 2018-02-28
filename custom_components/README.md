# Custom components, community contributions and overrides


## Community components

### [`🎦 ./display/`](display)

Interact with Android devices running the [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser) by using this third-party [Display](https://github.com/daemondazz/homeassistant-displays) platform.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-kiosk.png" alt="Kiosk card" title="Kiosk control" width="325">
        </div>
        <figcaption>
            <strong>Kiosk control.</strong>
        </figcaption>
    </figure>
</div>


### [`🔺 ./light/aurora.py`](light/aurora.py)

Opens communication with the [Nanoleaf Aurora](https://nanoleaf.me) using this [Hass.io-compatible fork](https://github.com/Oro/home-assistant/tree/light-aurora) of this [original component](https://github.com/software-2/ha-aurora).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-aurora.png" alt="Nanoleaf Aurora card" title="Nanoleaf Aurora control" width="325">
        </div>
        <figcaption>
            <strong>Nanoleaf Aurora control.</strong>
        </figcaption>
    </figure>
</div>


### [`📺 ./light/lightpack.py`](light/lightpack.py)

Supports basic operation of [Prismatik](https://github.com/psieg/Lightpack) monitor bias lighting using [Lightpack](https://github.com/kklemm91/Lightpack-HASS).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-lightpack.png" alt="Lightpack card" title="Lightpack control" width="325">
        </div>
        <figcaption>
            <strong>Lightpack control.</strong>
        </figcaption>
    </figure>
</div>


### [`💀 ./sensor/doomsday_clock.py`](sensor/doomsday_clock.py)

A local copy of my depressing [Doomsday Clock](https://github.com/renemarc/home-assistant-custom-components) component that tracks the _Bulletin of the Atomic Scientists_' [Minutes to Midnight](https://thebulletin.org/timeline) humanity status indicator.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-doomsday.png" alt="Doomsday Clock card" title="Doomsday Clock" width="325">
        </div>
        <figcaption>
            <strong>Doomsday Clock.</strong>
        </figcaption>
    </figure>
</div>


### [`❓ ./variable.py`](variables.py)

The missing link that allows storage of non-boolean values using the [Variable](https://github.com/rogro82/hass-variables) component.


## Overriden components

These are default Home Assistant components that were copied from the core to alter their behaviour. These changes really should be turned into appropriate [PRs](https://github.com/home-assistant/home-assistant/pulls).

### [`🚌 ./sensor/gtfs.py`](sensor/gtfs.py)

[GTFS](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/gtfs.py) public transit schedules component:
- Added support for next bus departures.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-transit.png" alt="Public Transit group" title="Public Transit" width="325"></a>
        </div>
        <figcaption>
            <strong>Public Transit group with schedules for the next three departures in two directions. Got to catch that bus! 🚌🏃</strong>
        </figcaption>
    </figure>
</div>
