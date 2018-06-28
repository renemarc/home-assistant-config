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
        <a href="#-sensoreboxpy" title="EBOX"><img src="../www/screenshots/group-network.png" alt="Network group" width="140"></a>
    </div>
    <div align="center">
        <a href="#-display" title="Kiosk"><img src="../www/screenshots/card-kiosk.png" alt="Kiosk card" width="140"></a>
        <a href="#-lightlightpackpy" title="Lightpack"><img src="../www/screenshots/card-lightpack.png" alt="Lightpack card" width="140"></a>
        <a href="#-sensordoomsday_clockpy" title="Doomsday Clock"><img src="../www/screenshots/card-doomsday.png" alt="Doomsday Clock card" width="140"></a>
    </div>
</figure>


<h1 align="center">Custom components, community contributions, and overrides</h1>

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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


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

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


### [`💀 ./sensor/doomsday_clock.py`](sensor/doomsday_clock.py)

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


### [`❓ ./variable.py`](variables.py)

The missing link that allows storage of non-boolean values using the [Variable component](https://github.com/rogro82/hass-variables).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


## Overriden components

These are default Home Assistant components that were copied from the core to alter their behaviour. These changes really should be turned into appropriate [PRs](https://github.com/home-assistant/home-assistant/pulls).


### [`📡 ./sensor/ebox.py`](sensor/ebox.py)

[Ebox](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/ebox.py) ISP data consumtion component:
- Upgraded [pyebox](https://github.com/titilambert/pyebox/) dependency to [support unlimited data packages](https://github.com/titilambert/pyebox/issues/1).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-network.png" alt="Network group" title="Network" width="325">
        </div>
        <figcaption>
            <p><strong>Network group.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


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


<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
