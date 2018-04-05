# Themes

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


### [`🌜 ./dark.yaml`](dark.yaml)

Automtically set by [`/automations/theme_auto.yaml`](../automations/theme_auto.yaml) whenever `input_boolean.night_mode` is enabled. Based on [PmxMononight](https://community.home-assistant.io/t/share-your-themes/22018/38) by PhysicalMagic.

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
