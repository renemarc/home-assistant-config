# UI views and groups

To avoid a mess of sensors, the state cards are placed into different pages (views), based on a simple architecture. The goal is always to present only as much info as needed, and data presented must be easy to find and consume.


## Organization

Views are split into 5 pages, organized in a similar fashion as [`/appdaemon/dashboards/`](../appdaemon/dashboards) only with more administrative features.


### [`🏠 ./default.yaml`](default.yaml)

With regular actions, climate control, bus schedules and a pretty picture of the day.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/menu-home.png" alt="Home menu option" title="Home" width="650">
        </div>
        <div>
            <img src="../www/screenshots/group-calendar.png" alt="Date group" title="Calendar" width="325">
            <img src="../www/screenshots/group-presence.png" alt="Presence group" title="Presence" width="325">
            <img src="../www/screenshots/group-climate.png" alt="Climate Control group" title="Climate Control" width="325">
            <img src="../www/screenshots/group-security.png" alt="Security Status group" title="Security Status" width="325">
            <img src="../www/screenshots/group-actions.png" alt="Actions group" title="Actions" width="325">
            <img src="../www/screenshots/group-transit.png" alt="Public Transit group" title="Public Transit" width="325">
        </div>
        <figcaption>
            <p><strong>Default view groups.</strong></p>
        </figcaption>
    </figure>
</div>


### [`🔘 ./switchboard.yaml`](switchboard.yaml)

Organized by room and control zone.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/menu-switchboard.png" alt="Switchboard menu option" title="Switchboard" width="650">
        </div>
        <div>
            <img src="../www/screenshots/group-kitchen.png" alt="Kitchen group" title="Kitchen" width="325">
            <img src="../www/screenshots/group-ceiling.png" alt="Ceiling Wash Lights group" title="Ceiling Wash Lights" width="325">
            <img src="../www/screenshots/group-lounge.png" alt="Lounge group" title="Lounge" width="325">
            <img src="../www/screenshots/group-bedroom.png" alt="Bedroom group" title="Bedroom" width="325">
            <img src="../www/screenshots/group-washroom.png" alt="Washroom group" title="Washroom" width="325">
        </div>
        <figcaption>
            <p><strong>Switchboard view groups.</strong></p>
        </figcaption>
    </figure>
</div>


### [`🌦 ./weather.yaml`](weather.yaml)

With current conditions, forecasts, air quality, radar and satellite maps.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/menu-weather.png" alt="Weather menu option" title="Weather" width="650">
        </div>
        <div>
            <img src="../www/screenshots/group-weather.png" alt="Today's Weather group" title="Today's Weather" width="325">
            <img src="../www/screenshots/group-forecast.png" alt="Weekly Forecast group" title="Weekly Forecast" width="325">
            <img src="../www/screenshots/card-radar-rain.png" alt="Environment Canada rain radar map" title="Environment Canada Rain" width="325">
            <img src="../www/screenshots/card-radar-snow.png" alt="Environment Canada snow radar map" title="Environment Canada Snow" width="325">
            <img src="../www/screenshots/card-satellite-geocolour.jpg" alt="NOAA GeoColour satellite image" title="NOAA GeoColour" width="325">
            <img src="../www/screenshots/card-satellite-vapour.jpg" alt="NOAA Water Vapour satellite image" title="NOAA Water Vapour" width="325">
            <img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Atmospheric Safety" width="325">
        </div>
        <figcaption>
            <p><strong>Weather view groups.</strong></p>
        </figcaption>
    </figure>
</div>


### [`👀 ./status.yaml`](status.yaml)

Geeky details about Home Assistant, network, battery status and per-location temperature and humidity.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/menu-status.png" alt="Status menu option" title="Status" width="650">
        </div>
        <div>
            <img src="../www/screenshots/group-system.png" alt="System group" title="System" width="325">
            <img src="../www/screenshots/group-network.png" alt="Network group" title="Network" width="325">
            <img src="../www/screenshots/group-temperature.png" alt="Temperature group" title="Temperature" width="325">
            <img src="../www/screenshots/group-humidity.png" alt="Humidity group" title="Humidity" width="325">
            <img src="../www/screenshots/group-battery.png" alt="Battery group" title="Battery levels" width="325">
        </div>
        <figcaption>
            <p><strong>Status view cards.</strong></p>
        </figcaption>
    </figure>
</div>


### [`⚙ ./configuration.yaml`](configuration.yaml)

States and automation overrides.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/menu-configuration.png" alt="Configuration menu option" title="Configuration" width="650">
        </div>
        <div>
            <img src="../www/screenshots/group-modes.png" alt="Modes group" title="Modes" width="325">
            <img src="../www/screenshots/group-configuration.png" alt="Configuration group" title="Configuration" width="325">
        </div>
        <figcaption>
            <p><strong>Some configuration view cards.</strong></p>
        </figcaption>
    </figure>
</div>


## Other

### [`🙈 ./invisible.yaml`](invisible.yaml)

For logical groups referenced in code but not displayed in views.


## Customization

The bulk of the customization is done in [`/customize.yaml`](../customize.yaml) and [`/customize_glob.yaml`](../customize_glob.yaml).

The looks of many state cards depend on Custom UI and other templates in [`/www/custom_ui/`](../www/custom_ui).
