# UI views and groups

To avoid a mess of sensors, the state cards are placed into different pages (views), based on a simple architecture. The goal is always to present only as much info as needed, and data presented must be easy to find and consume.


## Organization

Views are split into 5 pages, organized in a similar fashion as [`/appdaemon/dashboards`](../appdaemon/dashboards) only with more administrative features.


### Default page [`default.yaml`](default.yaml)

With regular actions, climate control, bus schedules and a pretty picture of the day.


### Switchboard [`switchboard.yaml`](switchboard.yaml)

Organized my room and control zone.


### Weather [`weather.yaml`](weather.yaml)

With current conditions, forecasts, air quality, radar and satellite maps.

<p align="center">
    <img src="../screenshots/ui-current-conditions@2x.png" alt="Current conditions" width="325">
    <img src="../screenshots/ui-weekly-forecast@2x.png" alt="Forecast" width="325">
</p>

### Status [`status.yaml`](status.yaml)

Geeky details about Home Assistant, network, battery status and per-location temperature and humidity.


### Configuration [`configuration.yaml`](configuration.yaml)

States and automation overrides.


## Customization

The bulk of the customization is done in [`/customize.yaml`](../customize.yaml) and [`/customize_glob.yaml`](../customize_glob.yaml).

The looks of many state cards depend on Custom UI and other templates in [`/www/custom_ui`](../www/custom_ui).
