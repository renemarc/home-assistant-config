# Modes and Flags Automations

This directory gathers all automations related to defining the states of modes and flags, essentially booleans used as master switches.

<div align="center">
    <figure>
        <div>
            <img src="../../www/screenshots/group-modes.png" alt="Modes and flags automations" title="Modes and flags" width="325">
        </div>
        <figcaption>
            <p><strong>Modes and flags automations.</strong></p>
        </figcaption>
    </figure>
</div>


## Modes logic explained

Like wild horses being released 🐎, all lights and devices will naturally run free unless harnessed. The modes are these harnesses.

Modes are the main published flags used to give higher-level directives to subscriber automations. An intent is broadly defined by a given flag, but the actual work, logic and know-how is handled by subscribers, say by [`/automations/areas/`](../areas/) or [`/automations/devices/`](../devices/).

This being a semi-open space one-bedroom apartment, I have set up the following five modes, defined in [`/misc/input_booleans.yaml`](../misc/input_booleans.yaml):

- **Low-power mode**: Reduce energy expenditure and light output; for instance during bright daytime or warm summer evenings.
- **Nap mode**: Someone wants to take a nap or sleep, potentially without preventing a partner from being busy.
- **Night mode**: Shut off all non-bedroom indoor lights.
- **Quiet mode**: Disruptive noise sources should be muted; think notifications and background noisemakers, not actively-controlled TV or music.
- **Scene mode**: A global scene has been set, don't let scheduled effects disturb it!

So, when preparing to go to sleep one can turn off all non-bedroom indoor lights using a [Flic](https://flic.io/) button long-press on the nightstand. Then when everyone is ready to actually sleep, a single click of the Flic button closes bedroom lights. When waking-up, the same Flic button presses will disable the related modes to allow lights and devices to run as they should.

In the interest of redundancy and convenience, mode control is also available using [HomeKit](https://www.home-assistant.io/components/homekit/) controllers (iPhones), a centralized wallmounted Android tablet in kiosk-mode (see [`/appdaemon/dashboards/`](../..//appdaemon/dashboards/)), an Aeotec minimote (now discontinued) and of course the [Home Assistant UI](https://www.home-assistant.io/docs/frontend/).


## Modes

### [`🔅️ ./low_mode_start.yaml`](low_mode_start.yaml)

Enable low-power state for a more relaxed environment. **Auto-start disabled.**


### [`🔆️ ./low_mode_stop.yaml`](low_mode_stop.yaml)

Disable low-power state. **Auto-start disabled.**


### [`😴️ ./nap_mode_start.yaml`](nap_mode_start.yaml)

When someone takes a nap.

Subscribers should shut off bedroom lights, lower potentially disruptive light sources elsewhere, and minimize noises without preventing someone else from being active.


### [`😃️ ./nap_mode_stop.yaml`](nap_mode_stop.yaml)

When someone ends their nap.


### [`🌌️ ./night_mode_start.yaml`](night_mode_start.yaml)

Enable night (dark) mode.

Subscribers should shut off all non-essential indoor lights and noise sources, except for bedroom devices which should respond to [`nap_mode_start.yaml`](nap_mode_start.yaml) instead.


### [`🌅️ ./night_mode_stop.yaml`](night_mode_stop.yaml)

Disable night (dark) mode.


### [`🔇 ./quiet_mode_start.yaml`](quiet_mode_start.yaml)

When noise makers should not be running.

Subscribers should quiet down noisy machines and mute non-critical alarms.


### [`🔊️ ./quiet_mode_stop.yaml`](quiet_mode_stop.yaml)

When noise makers should be allowed to run.


## Flags

### [`🏃‍♂️️ ./motion_auto.yaml`](motion_auto.yaml)

Toggle flag when motion is sensed or is no longer detected.


### [`🖐️️ ./tamper_start.yaml`](tamper_start.yaml)

Detect when perimeter device is being tempered with.


### [`🔄️ ./tamper_stop.yaml`](tamper_stop.yaml)

Reset flag when tampered devices have their own alarm reset.


## Customization

The bulk of the customization is done in [`/customize.yaml`](../../customize.yaml) and [`/customize_glob.yaml`](../../customize_glob.yaml).

The looks of many state cards depend on Custom UI and other templates in [`/www/custom_ui/`](../../www/custom_ui).
