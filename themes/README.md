# Themes

These CSS configurations serve to bonify the frontend's user interface and improve the user experience.


## [`normal.yaml`](normal.yaml) theme

Contains minor improvements over Home Assistant's [default theme](https://github.com/home-assistant/home-assistant-polymer/blob/master/src/resources/ha-style.html).


## [`dark.yaml`](dark.yaml) theme

Automtically set by [`/automations/theme_auto.yaml`](../automations/theme_auto.yaml) whenever `input_boolean.night_mode` is enabled. Based on [PmxMononight](https://community.home-assistant.io/t/share-your-themes/22018/38) by PhysicalMagic.


## [`card-secondary-title.yaml`](card-secondary-title.yaml) theme

Used in [`/customize.yaml`](../customize.yaml) to replace a sensor's title with its dynamic `extra-data-template`.


## [`card-warning.yaml`](card-warning.yaml) theme

Used in [`/customize_glob.yaml`](../customize_glob.yaml) to highlight a sensor in yellow whenever its state is within a range that should be of interest. Using transprency, it looks good in both normal and dark themes.


## [`card-critical.yaml`](card-critical.yaml) theme

Used to highlight a sensor in red whenever its state is within a critical range that should command attention. Compatible with both normal and dark themes.
