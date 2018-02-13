# Sensors

Eash YAML file groups together all related sensors and contains details on usage.

- [`calendar.yaml`](calendar.yaml): Everything time related.
- [`climate.yaml`](climate.yaml): Indoor climate conditions.
- [`gtfs.yaml`](gtfs.yaml): [General Transit Feed Specification](http://gtfs.org), essentially bus schedules. See also [`/gtfs`](../gtfs) for performance tuning of this large dataset.
- [`health.yaml`](health.yaml): [Atmospheric pollution](https://waqi.info/), UV Index and [chances of Armageddon](https://thebulletin.org/timeline).
- [`image.yaml`](image.yaml): Data sources for some [`/cameras`](../cameras).
- [`isp.yaml`](isp.yaml): Internet service provider consumption details.
- [`light.yaml`](light.yaml): Reports on loaded effects for smart ligths.
- [`misc.yaml`](misc.yaml): Everything else.
- [`network.yaml`](network.yaml): Internet connection speed and latency testing. 
- [`power.yaml`](power.yaml): Battery states.
- [`system.yaml`](system.yaml): Geeky details on HASS and its hardware status.
- [`weather.yaml`](weather.yaml): Everything weather related.


## Usage

Some sensors are used for information display only in [groups](../groups) and [dashboards](../appdaemon/dashboards), while others are also used for [automations](../automations).


## Customization

The bulk of the customization is done in [`/customize.yaml`](../customize.yaml) and some in [`/customize_glob.yaml`](../customize_glob.yaml).
