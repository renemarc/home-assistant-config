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

## Integrations

These are essentially used as triggers and conditions for [`/automations/`](../automations).

### [` ./homekit.yaml`](homekit.yaml)

### [`💡 ./lifx.yaml`](lifx.yaml)

### [`▶️ ./plex.yaml`](plex.yaml)

### [`🚄 ./speedtest.yaml`](speedtest.yaml)

### [`⚡ ./tplink.yaml`](tplink.yaml)

### [`📶 ./unifi.yaml`](unifi.yaml)

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

### [`🏘️ ./groups.yaml`](groups.yaml)

Groups are used in [`/automations`](../automations) and [`/scripts`](../scripts) in order to reduce redundancy and ease maintenance.

### [`📽 ./media_players.yaml`](media_players.yaml)

For [Kodi](https://kodi.tv) and [Plex](https://www.plex.tv).

### [`👥 ./persons.yaml`](persons.yaml)

### [`⏺️ ./recorder.yaml`](recorder.yaml)

### [`🌈 ./scenes.yaml`](scenes.yaml)

Simple registration for [LIFX's server-based scenes](https://www.lifx.com/pages/themes-scenes), see [`/lights/`](../lights#lifx-smart-wi-fi-lights) for more details. All other scenes are implemented as [`/scripts/`](../scripts) in order to access more advanced features.

### [`🐚 ./shell_commands.yaml`](shell_commands.yaml)

Reusable command-line directives when no component exists or provides these options reliably.

Connects to the UniFi controller with a read-only user.

### [`⛅ ./weather.yaml`](weather.yaml)

### [`🗺 ./zones.yaml`](zones.yaml)

Used for presence tracking and automations based on user distance from key locations.

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
