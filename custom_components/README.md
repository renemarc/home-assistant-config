# Custom components, community contributions and overrides


## Community components

- [`light/aurora.yaml`](light/aurora.yaml) opens communication with the [Nanoleaf Aurora](https://nanoleaf.me) using this [Hass.io-compatible fork](https://github.com/Oro/home-assistant/tree/light-aurora) of this [original component](https://github.com/software-2/ha-aurora).
- [`light/lightpack.yaml`](light/lightpack.yaml) supports basic operation of [Prismatik](https://github.com/psieg/Lightpack) monitor bias lighting using [Lightpack](https://github.com/kklemm91/Lightpack-HASS)
- [`sensor/doomsday_clock.yaml`](sensor/doomsday_clock.yaml) is a local copy of my depressing [Doomsday Clock](https://github.com/renemarc/home-assistant-custom-components) component.
- [`variable.yaml`](variables.yaml) is the missing link that allows storage of non-boolean values using the [Variable](https://github.com/rogro82/hass-variables) component.


## Overriden components

- [`sensor/ebox.yaml`](sensor/ebox.yaml): [EBox](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/ebox.py)
    + Added support for "unlimited" values.
- [`sensor/gtfs.yaml`](sensor/gtfs.yaml): [GTFS](https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/sensor/gtfs.py)
    + Added support for next bus departures.
