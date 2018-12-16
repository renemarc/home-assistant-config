<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **misc** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#miscellaneous" title="Miscellaneous
(Scene from the movie Modern Times)"><img src="https://media.giphy.com/media/VP5UwVic0l7W0/giphy.gif" alt="Charlie Chaplin fixing a machine in Modern Times"></a>
    </div>
</figure>

<h1 align="center">Miscellaneous</h1>

This folder gathers all simpler configuration files.

## Inputs

These are essentially used as triggers and conditions for [`/automations/`](../automations).

### [`✅ ./input_booleans.yaml`](input_booleans.yaml)

Modes and other binary intermediary state holders for [`/automations/`](../automations).

### [`🔲 ./input_selects.yaml`](input_selects.yaml)

List of light effects and global scenes for the frontend and for [`/appdaemon/dashboards/`](../appdaemon/dashboards).

### [`❓ ./variables.yaml`](variables.yaml)

Flexible intermediary data holder, using the [third-party](https://github.com/rogro82/hass-variables) [`/custom_components/varyable.py`](../custom_components/varyable.py).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Other

### [`🔘 ./binary_sensors.yaml`](binary_sensors.yaml)

Essentially used for [Flic buttons](https://flic.io) and [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser) motion sensor.

### [`🔢 ./counters.yaml`](counters.yaml)

Currently used by some [`/automations/notifications`](../automations/notifications) to limit the number of consecutive notifications sent out, in order to avoid nagging when action cannot immediately be taken (say, while we are out of town).

### [`📍 ./device_trackers.yaml`](device_trackers.yaml)

For tracking device presence with ~~Bluetooth and~~ a [UniFi](https://www.ubnt.com/unifi/unifi-cloud-key/) wireless access point.

### [`🎦 ./displays.yaml`](displays.yaml)

To enable basic control of the [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser) using the [third-party](https://github.com/daemondazz/homeassistant-displays) [`/custom_components/display/`](../custom_components/display) component.

### [`📽 ./media_players.yaml`](media_players.yaml)

For [Kodi](https://kodi.tv) and [Plex](https://www.plex.tv).

### [`🌈 ./scenes.yaml`](scenes.yaml)

Simple registration for [LIFX's server-based scenes](https://www.lifx.com/pages/themes-scenes), see [`/lights/`](../lights#lifx-smart-wi-fi-lights) for more details. All other scenes are implemented as [`/scripts/`](../scripts) in order to access more advanced features.

### [`🐚 ./shell_commands.yaml`](shell_commands.yaml)

Reusable command-line directives when no component exists or provides these options reliably.

### [`🗺 ./zones.yaml`](zones.yaml)

Used for presence tracking and automations based on user distance from key locations.

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
