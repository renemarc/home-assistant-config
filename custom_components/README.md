# Custom components, community contributions and overrides


## Community components

### [`🎦 ./display/`](display)

Interact with Android devices running the [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser) by using this third-party [Display platform](https://github.com/daemondazz/homeassistant-displays).

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


### [`📺 ./light/lightpack.py`](light/lightpack.py)

Supports basic operation of [Prismatik](https://github.com/psieg/Lightpack) monitor bias lighting using this [Lightpack component](https://github.com/kklemm91/Lightpack-HASS).

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


### [`💀 ./sensor/doomsday_clock.py`](sensor/doomsday_clock.py)

A local copy of my depressing [Doomsday Clock component](https://github.com/renemarc/home-assistant-custom-components) that tracks the _Bulletin of the Atomic Scientists_' [Minutes to Midnight](https://thebulletin.org/timeline) humanity status indicator.

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


### [`❓ ./variable.py`](variables.py)

The missing link that allows storage of non-boolean values using the [Variable component](https://github.com/rogro82/hass-variables).


## Overriden components

These are default Home Assistant components that were copied from the core to alter their behaviour. These changes really should be turned into appropriate [PRs](https://github.com/home-assistant/home-assistant/pulls).


### [`📡 ./sensor/ebox.py`](sensor/ebox.py)

[Ebox](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/ebox.py) ISP data consumtion component:
- Upgraded [pyebox](https://github.com/titilambert/pyebox/) dependency to [support unlimited data packages](https://github.com/titilambert/pyebox/issues/1).


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
