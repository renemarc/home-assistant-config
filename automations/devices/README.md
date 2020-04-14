<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / [automations](..) / **devices** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#wall-mounted-dashboard" title="Wall-mounted dashboard"><img src="../../www/screenshots/dashboard-main.gif" alt="Main dashboard" width="280"></a>
    </div>
    <div align="center">
        <a href="#bed" title="Bed"><img src="../../www/screenshots/group-bedroom.png" alt="Bedroom group" width="140"></a>
        <a href="limitlessled-kitchen-lights" title="LimitlessLED kitchen lights"><img src="../../www/screenshots/group-kitchen.png" alt="Kitchen group" width="140"></a>
        <a href="#nanoleaf-aurora" title="Nanoleaf Aurora"><img src="../../www/screenshots/card-aurora.png" alt="Nanoleaf Aurora card" width="140"></a>
        <a href="#lightpack-dynamic-tv-bias-light" title="Lightpack dynamic TV bias light"><img src="../../www/screenshots/card-lightpack.png" alt="Lightpack card" width="140"></a>
    </div>
</figure>

<h1 align="center">Devices automations</h1>

These are either simple binary units plugged into a smart outlet, or smart devices whose parameters that can be controlled with finer subtlety.

Only some devices requiring some independent control have automations, all others are handled as obedient slaves within [`/automations/areas/`](../areas/).

## Nanoleaf Aurora

[Aurora](https://nanoleaf.me) smart light panels in the lounge (see [`/lights/`](../../lights#nanoleaf-aurora-smart-light-panels)).

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/card-aurora.png" alt="Nanoleaf Aurora card" title="Nanoleaf Aurora control" width="325">
        </div>
        <figcaption>
            <p><strong>Nanoleaf Aurora control.</strong></p>
        </figcaption>
    </figure>
</div>

### [`🔆️ ./aurora_brightness.yaml`](aurora_brightness.yaml)

Change Nanoleaf Aurora's brightness.

### [`🌈 ./aurora_effect.yaml`](aurora_effect.yaml)

Change Nanoleaf Aurora based on its loaded-in effects.

The Aurora has effects in its internal memory that are programmed with the Nanoleaf mobile app. They have unique names, which are invoked to change the effect that is displayed on the panels.

### [`⏲️ ./aurora_schedule.yaml`](aurora_schedule.yaml)

Schedule the Nanoleaf Aurora based on its loaded-in effects.

Unless an effect is manually selected, this scheduler will do its thing.

### [`🔘️ ./aurora_select.yaml`](aurora_select.yaml)

Manually select a Nanoleaf Aurora built-in effect.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Bed

The bed has two sets of [LIFX Z RGBW lights strips](https://www.lifx.com/products/lifx-z) (see [`/lights/`](../../lights#lifx-z-rgbw-led-strips)), one underneath the frame and one behind the headboard. Groovy!

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/group-bedroom.png" alt="Bedroom group" title="Bedroom group" width="325">
        </div>
        <figcaption>
            <p><strong>Bedroom group.</strong></p>
        </figcaption>
    </figure>
</div>

### [`🌈 ./bed_effect.yaml`](bed_effect.yaml)

Change bed underglow lights based on [LIFX Cloud scenes](https://www.home-assistant.io/integrations/lifx_cloud/).

The LIFX strips have some effects programmed with the LIFX mobile app and stored on their servers. Each effect mentions which device will receive which colour pattern. Also, each effect has a UUID that can be used to load the effect from the servers and program the LIFX devices accordingly.

### [`⏲️ ./bed_schedule.yaml`](bed_schedule.yaml)

Schedule bed underglow lights based on LIFX Cloud scenes.

Unless an effect is manually selected, this scheduler will do its thing.

### [`🔘️ ./bed_select.yaml`](bed_select.yaml)

Manually select a LIFX cloud effect for the bed underglow lights.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Wall-mounted dashboard

See [`/appdaemon/dashboards`](../../appdaemon/dashboards).

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/dashboard-all.gif" alt="Dashboards in rotation" title="Dashboards in rotation">
        </div>
        <figcaption>
            <strong>Dashboards in rotation.</strong>
        </figcaption>
    </figure>
</div>

### [`⏯️ ./kiosk_auto.yaml`](kiosk_auto.yaml)

Toggle kiosk display.

### [`🔅 ./kiosk_low.yaml`](kiosk_low.yaml)

Toggle kiosk display's brightness.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## LimitlessLED kitchen lights

[LimitlessLED/MiLight](http://www.limitlessled.com) controllers are used to operate various high-CRI CCT LED strips in the kitchen (see [`/lights/`](../../lights#limitlessled-milight-controllers-with-high-cri-cct-led-strips)).

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/group-kitchen.png" alt="Kitchen group" title="Kitchen group" width="325">
        </div>
        <figcaption>
            <p><strong>Kitchen group.</strong></p>
        </figcaption>
    </figure>
</div>

### [`🔆️ ./kitchen_lights_full.yaml`](kitchen_lights_full.yaml)

Turn kitchen lights full on.

Set all kitchen lights to maximum brightness when Flic button is held.

### [`✨ ./kitchen_lights_init.yaml`](kitchen_lights_init.yaml)

Set kitchen lights to a known state.

LimitlessLED lights do not provide state information, so we force it depending on the current conditions.

### [`⏹ ./kitchen_lights_off.yaml`](kitchen_lights_off.yaml)

Turn off kitchen lights.

Turn off all kitchen lights when Flic button is single clicked.

### [`▶️ ./kitchen_lights_on.yaml`](kitchen_lights_on.yaml)

Turn on kitchen lights.

Turn on all kitchen lights when Flic button is single clicked.

### [`🔘️ ./kitchen_lights_toggle.yaml`](kitchen_lights_toggle.yaml)

Toggle kitchen lights.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Lightpack dynamic TV bias light

A DIY 100 LED dots Arduino setup running [Adalight](https://learn.adafruit.com/adalight-diy-ambient-tv-lighting) code is behind the television and connected to an HTPC, and is controlled by a [fork of Prismatik](https://github.com/psieg/Lightpack) (see [`/lights/`](../../lights#lightpack-dynamic-tv-bias-light)).

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/card-lightpack.png" alt="Lightpack card" title="Lightpack control" width="325">
        </div>
        <figcaption>
            <p><strong>Lightpack control.</strong></p>
        </figcaption>
    </figure>
</div>

### [`📺 ./lightpack_auto.yaml`](lightpack_auto.yaml)

Change Lightpack effect based on TV state.

Unless a scene is selected, set the Lightpack to react to the screen contents if the TV is on, otherwise set the bias light to something that is not distracting.

### [`🌈 ./lightpack_effect.yaml`](lightpack_effect.yaml)

Change Lightpack based on its programmed profiles.

The Lightpack is controlled by the Prismatik softwage, which allows for different profiles to be created and loaded at will. They have unique names, but let's use a translation map here to reduce name binding between Home Assistant and daily HTPC usage.

### [`🔘️ ./lightpack_select.yaml`](lightpack_select.yaml)

Manually select a Lightpack effect for the TV bias light.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Nightlights

A few strategically selected smart lights operate as motion-activated dim nightlights durong _night_ mode. Useful when someone needs to wake up and find the way to the bathroom at night without being blinded by full-on lights!

### [`⏹️ ./nightlight_off.yaml`](nightlight_off.yaml)

Turn off nightlights when no longer needed.

### [`▶️ ./nightlight_on.yaml`](nightlight_on.yaml)

Turn on nightlights when appropriate.

## Video players

Video players automations are linked to HTPC usage, and only run in response to the state of video players and their types of content.

### [`📺 ./tv_off.yaml`](tv_off.yaml)

Turn off the television if nobody seems to be home.

### [`▶️ ./video_player_resume.yaml`](video_player_resume.yaml)

Media player plays video content.

This automation will kick in only if video playback is starting/resuming on an HTPC media player. Playing audio or anything else will not trigger the action.

### [`⏸️️ ./video_player_stop.yaml`](video_player_stop.yaml)

Media player paused/stopped video content.

This automation only responds to the pausing/stopping of HTPC video playback. If music is playing on any HTPC media player then this automation will not perform its action.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Customization

The bulk of the customization is done in [`/ui-lovelace.yaml`](../../ui-lovelace.yaml), [`/customize.yaml`](../../customize.yaml), and [`/customize_glob.yaml`](../../customize_glob.yaml).

<!--
Footer starts.
-->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> this repo! 😃</strong></p>

[🔙 Back to `/automations/`](../)

[🏠 Home][link-repo]
<!--
Footer ends.
-->
