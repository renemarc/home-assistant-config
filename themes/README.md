<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **themes** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#-normalyaml"><img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Normal theme" width="140"></a>
        <a href="#-darkyaml"><img src="../www/screenshots/group-atmosphere-dark.png" alt="Atmospheric Safety group (dark theme)" title="Dark theme" width="140"></a>
    </div>
    <div align="center">
        <a href="#-card-secondary-titleyaml"><img src="../www/screenshots/card-secondary.png" alt="Secondary Title card" title="Secondary Title" width="140"></a>
        <a href="#-card-warningyaml"><img src="../www/screenshots/card-warning.png" alt="Warning card" title="Normal theme" width="140"></a>
        <a href="#-card-warningyaml"><img src="../www/screenshots/card-warning-dark.png" alt="Warning card (dark theme)" title="Dark theme" width="140"></a>
        <a href="#-card-criticalyaml"><img src="../www/screenshots/card-critical.png" alt="Critical card" title="Normal theme" width="140"></a>
        <a href="#-card-criticalyaml"><img src="../www/screenshots/card-critical-dark.png" alt="Critical card (dark theme)" title="Dark theme" width="140"></a>
    </div>
</figure>

<h1 align="center">Themes</h1>

These CSS configurations serve to bonify the frontend's user interface and improve the user experience.

## Whole themes

These full themes change the whole look of Home Assistant.

### [`🌞 ./normal.yaml`](normal.yaml)

Contains minor improvements over Home Assistant's [default theme](https://github.com/home-assistant/home-assistant-polymer/blob/master/src/resources/ha-style.html).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Normal theme" width="325">
        </div>
        <figcaption>
            <p><strong>Normal theme.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🌜 ./dark.yaml`](dark.yaml)

Automtically set by [`/automations/theme_auto.yaml`](../automations/theme_auto.yaml) whenever **night_mode** in [`/misc/input_booleans.yaml`](../misc/input_booleans.yaml) is enabled. Based on [PmxMononight](https://community.home-assistant.io/t/share-your-themes/22018/38) by PhysicalMagic.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/group-atmosphere-dark.png" alt="Atmospheric Safety group (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Dark theme.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Card themes

These focused themes are used when modifying the display of specific sensors only.

### [`🥈 ./card-secondary-title.yaml`](card-secondary-title.yaml)

Used in [`/customize.yaml`](../customize.yaml) to replace a sensor's title with its dynamic `extra-data-template` when a component does not provide a `friendly_name_template` variable like the [template sensor](https://home-assistant.io/components/sensor.template/) does.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-secondary.png" alt="Secondary Title card" title="Secondary Title" width="325">
        </div>
        <figcaption>
            <p><strong>Secondary Title card, used to replace the sensor name with the temperature's value.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⚠ ./card-warning.yaml`](card-warning.yaml)

Used in [`/customize_glob.yaml`](../customize_glob.yaml) to highlight a sensor in yellow whenever its state is within a range that should be of interest. Using transprency, it looks good in both normal and dark themes.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-warning.png" alt="Warning card" title="Normal theme" width="325">
            <img src="../www/screenshots/card-warning-dark.png" alt="Warning card (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Warning card.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🚨 ./card-critical.yaml`](card-critical.yaml)

Used to highlight a sensor in red whenever its state is within a critical range that should command attention. Compatible with both normal and dark themes by also using transparency.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-critical.png" alt="Critical card" title="Normal theme" width="325">
            <img src="../www/screenshots/card-critical-dark.png" alt="Critical card (dark theme)" title="Dark theme" width="325">
        </div>
        <figcaption>
            <p><strong>Critical card.</strong></p>
        </figcaption>
    </figure>
</div>

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
