# René-Marc's Home Assistant configuration

Configuration for Home Assistant running Hass.io on a Raspberry Pi for a one bedroom apartment, offering convenience automations over lights and climate while providing multiple intuitive user controls.


## Contents
1. **[Overview](#overview):** [User stories](#user-stories), [Goals](#goals). 
1. **[Key features](#Goals):** [Climate control](#climate-control), [Weather report](#weather-report), [Lighting control](#lighting-control), [Presence](#presence), [Scenes and actions](#scenes-and-actions), [General information](#general-information), [Human interfaces](#human-interfaces). 
1. **[Task list](#task-list):** [Work in progress](#work-in-progress), [Backlog](#backlog), [Wishlist](wWishlist). 
1. **[Setup](#setup):** [System and interfaces](#system-and-interfaces), [Devices and sensors](#devices-and-sensors), [Software](#software), [Hass.io add-ons](#hassio-add-ons). 
1. **[Thanks](#thanks)**.


## Overview

### User stories
- **As a resident** I want a reliable home automation platform to handle lights and climate that can easily be controlled and overridden in many intuitive ways.
- **As an apartment dweller** I want to have a discrete, non-permanent installation that takes as little space as possible.
- **As a developer** I want to use an open-source platform that is feature-rich, accessible, flexible and actively maintained.
- **As a consumer** I want to pick and choose which devices I wish to acquire without necessarily being locked into a closed ecosystem.
- **As a couple** we want to be able to control lights and get quick overview of weather forecasts and public transit schedules through simple to use interfaces.

### Goals
- **Inconspicuous**: I like tech alright, but like good butlers it should stay out of sight but summonable when desired. Think Fiji villa, not server room.
- **Modular**: Both code and devices should be easily replaceable.
- **Internet independent**: As much local processing as possible for the essential features.
- **Accessible through multiple ways:** Computers, tablet (kiosk), voice, smart phones, buttons.
- **Intuitive user interfaces:** One look as a group of sensors/switches should be sufficient for anyone to understand the current conditions and how to operate an interface.
- **Redundant controls:** Multiple interfaces should be able to control devices without interference, and state changes from manual interventions or dedicated manufacturer apps should be tracked when possible.
- **No information overload:** Provide just enough insight to get an ideas of what's going on. And no need for data that's best consumed on more interactive devices (like stock prices, Steam community status)
- **Not everything should be networked:** Bathroom fan, pantry and laundry room lights have their independent motion sensors and that's a good thing. Same with the smoke detector, because I sure don't want to require extensive skin grafts because I forgot an extra space in a YAML file. Eek!
- **No Alexa/Cortana/Google Voice:** I don't want to have advertising agencies, online stores, or other AI-feeding Big Brother tech-monsters listening in to everything we say just for the dubious convenience of turning on a light using my voice.


## Key features

### Climate control
- **Temperature monitoring**, averaged to compensate for sensor calibration inaccuracies, then rounded.
- **Humidity monitoring**, also averaged and rounded.
- **Turn dehumidifier on/off when needed**, based on humidity averaged from multiple sensors, and only during the afternoon so not to bother anyone.
- **Turn dehumidifier off when windows/door opened are opened**, instantly for windows and after 5 minutes for doors.
- **Low/High humidity status and alerts**, in case something is wrong with the dehumidifier or the eventual humidifier.
- **Mold conditions status and alert**, in case dehumidifier is full/overwhelmed or someone transformed the place into a steam room. Again.

### Weather report
- **Easy to read status and forecasts** using Dark Sky data and only showcasing parameters that actually matter.
- **Outdoor quality monitoring** with numeric levels and human-friendly categorization for ozone, carbon monoxide, nitrogen dioxide, 2.5μm particulate matter and UV light, averaged from multiple surrounding local stations.
- **Weather radar and satellite maps** for [local rain and snow](https://weather.gc.ca/radar/index_e.html) from Environment Canada and [regional air masses](http://www.nhc.noaa.gov/satellite.php) from the U.S. National Oceanic and Atmospheric Administration.

### Lighting control
- **Control for all pluggable lights**, dumb and smart.
- **Nanoleaf Aurora control**:
    + Manual theme selection.
    + Automatically rotate through device-based themes based on time of day (unless manually selected above).
- **LIFX Z ceiling wash lights control**:
    + Manual theme selection.
    + Automatically rotate through cloud-based themes based on time of day (unless manually selected above).
- **Automatically correlated color temperature (CCT)**, for [f.lux](https://justgetflux.com/)-like white temperature shift to gradually remove blue light based on a custom color and brightness curve and preset active hours, not daylight.
- **Presence-based nightlights**, where strategic lights fade in, dimmed very low, when walking around at night, say when someone wakes up to go the bathroom.

### Presence
- **Front door binary sensor**, to know if someone left the door open.
- **Front door indicator in shower** where the shower stall's light changes color briefly and subtly when front door opens/closes, to indicate a showering partner that the better half left or came in.

### Scenes and actions
- **Good morning** action where all lights turn on gradually, and noise-making devices are allowed to run if needed.
- **Nap time** action where that fade out lights in and near bedroom, turn off noise makers.
- **Good night** action fade out all lights outside of bedroom.
- **Movie scene** turn on ambiance light and dim smart lights when playing a movie, then return to standard automations when pausing/stopping.

### General information
- **[Local bus schedules](https://home-assistant.io/components/sensor.gtfs/)** with next 3 departures.
- **[Doomsday Clock](https://thebulletin.org/timeline)** in case egocentric psychopaths keep on playing Russian roulette with humanity's future. 
- **Network status monitoring** for latency, upspeed, downspeed.
- **Home Assistant status monitoring** for geek cred with average load, RAM use, disk use, uptime, and update availability.

### Human interfaces
- **Flic button on nightstand** for wake-up, sleep time, and nightstand light control, depending on current state and click sequence.
- **[Homebridge](https://github.com/nfarina/homebridge)** for using some key sensors and devices with iPhones (only if using the same VLAN though).
- **[Home Assistant Companion](https://itunes.apple.com/us/app/home-assistant-companion/id1099568401?mt=8) iPhone app** for full UI access in the palm of your hand. Muahahaha!
- **[HADashboard](https://home-assistant.io/docs/ecosystem/hadashboard/)** for wall-mounted tablet, featuring indoor sensors reports, transit schedules, weather forecast and radar maps, wrapped in an obvious navigation scheme for much UX goodness. You'll like!


### Task list

#### Work in progress
- Dashboard: daily picture slideshow

#### Backlog
- UI: State card for text only (weather, quotes...)
- Component: fix unlimited bandwidth consumption bug
- Status: Update available.
- Scene: Romantic
- Scene: Gaming/Party
- Dashboard: finish main panel
- Dashboard: organize status panel
- Dashboard: adjust sensors refresh rate
- Interface: Overrides for each automation
- Interface: Voice command (snips.ai)
- Automation: Away mode
- Presence detection: Cellphones
- Presence detection: Router
- Contribute: GTFS sensor optimization and documentation
- Contribute: HADashboard widget optimizations

#### Wishlist
- Dashboard: context-aware link widgets
- Automation: Welcome home front door trigger
- Automation: Door/Window sensor temper alert
- Component: UPS monitoring
- Component: Read rooftop weather station (Fine Offset WH1080)
- Network: use USB gigabit connection to test above 80MB/s downspeeds
- Device: Increase nightlight movement detection coverage
- Device: LIFX Z strips under bed
- Device: Kitchen under-cabinet lighting
- Device: Flic button (kitchen)
- Device: Window binary sensors
- Device: Indoor air quality sensing and report
- Device: Exterior light
- Device: Monitor humidity in humidor
- Device: Light patterns in windowed cabinets
- Device: Motion nightlight in bathroom under mirror
- Device: Fade in/out fairy lights and bedside lamp
- Device: Timer-based, fade in/out, twinkling Christmas tree


## Setup

### Supporting hardware choices
- **Ubiquiti router and access point** because forking over some dough for reliable, rock-solid prosumer networking gear makes everything run smoothly. And because hearing one less complaint (dropped wifi signal) from the girlfriend is priceless. \*sigh\*
- **Uninterruptible power supply** to ride over transient power failures.
- **Z-Wave** for reliability and guaranteed interoperability between vendors (unlike Zigbee...)
- **Wifi** for its cheapness, omnipresence and non requirement for vendor-specific hubs.

### Configuration
- **Dedicated VLAN** (Virtual LAN) to segregate all IoT devices from other devices ...because I cannot trust that my vacuum cleaner won't go on a killing spree. Remember [Runaway with Tom Selleck](http://www.imdb.com/title/tt0088024/)? Eek!
- **Local static IPs** for all devices to avoid random drops.
- **Local development** on a local virtual machine using Docker, then pushed by GIT to a Raspberry Pi.
- **Shareable code** with all identifiers kept in a non-committed, secrets file.

### System and interfaces
- **[Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)** running Hass.io.
- **[Aeotec Z-Stick Gen5](https://aeotec.com/z-wave-usb-stick)** Z-Wave USB dongle.
- **[NooElec NESDR SMArt](http://www.nooelec.com/store/nesdr-smart.html)** RTL-SDR (software-defined radio) USB dongle for reading AcuRite sensors.
- **[Acer Iconia One 10" tablet](https://www.acer.com/ac/en/CA/content/series/iconiaone10)** (1280x800 IPS screen) wallmounted as a kiosk.

### Devices and sensors
- **[Nanoleaf Aurora](https://nanoleaf.me/en-ca/)** light panels kit. Pretty!
- **[LIFX+](https://www.lifx.com/products/lifx-plus)** A19 RGB light bulb (x2).
- **[LIFX Z](https://www.lifx.com/products/lifx-z-starter-kit-without-homekit)** light strip without HomeKit as ceiling wash lights (x3).
- **[Flic](https://flic.io/)** bluetooth button.
- **[Aeotec Door / Window Sensor Gen5](https://aeotec.com/z-wave-door-window-sensor)** for front door.
- **[Aeotec MultiSensor 6](https://aeotec.com/z-wave-sensor)** for temperature/humidity/presence detection.
- **[Adalight](https://learn.adafruit.com/adalight-diy-ambient-tv-lighting)** DIY 100-dots TV backlighting controlled by [Lightpack+Prismatik](https://github.com/psieg/Lightpack) on HTPC.
- **[AcuRite 06044M Wireless Sensor](https://www.acurite.com/indoor-temperature-sensor-and-humidity-gauge.html)** for cheap temperature and humidity monitoring.
- **[TP-Link Smart Wi-Fi Plug Mini outlets](http://www.tp-link.com/us/products/details/cat-5516_HS105.html)** to control dumb devices (x6).
- **[Frigidaire dehumidifier](http://www.dehumidifierbuyersguide.com/frigidaire-ffad7033r1-review/)** via TP-Link wifi outlet.
- **Oscillating fan** via TP-Link wifi outlet.
- **Fairy lights** via TP-Link wifi outlets (x3).
- **DIY LED nightstand** via TP-Link wifi outlet.

### Software
- **[Hass.io](https://home-assistant.io/)** on Raspberry Pi (production setup).
- **[Docker](https://www.docker.com/)** on local machine (for development).

### Hass.io add-ons
- **[AppDaemon2](https://github.com/home-assistant/appdaemon)** for HADashboard tablet UI.
- **[Bluetooth BCM43xx](https://home-assistant.io/addons/bluetooth_bcm43xx/)** to use Raspberry Pi's bluetooth.
- **[Flicd](https://github.com/pschmitt/hassio-addons)** to connect with Flic bluetooth buttons.
- **[Mosquitto MQTT broker](https://home-assistant.io/addons/mosquitto/)** for standard IoT messaging.
- **[Homebridge](https://github.com/hassio-addons/addon-homebridge)** to control non-HomeKit compatible devices using iPhones.
- **[RTL_433 to MQTT Bridge](https://github.com/james-fry/hassio-addons/)** to receive and decode AcuRite radio signals.
- **[Samba share](https://home-assistant.io/addons/samba/)** for configuration file sharing.

## Thanks

Kudos to:
- **The [dedicated core team](https://home-assistant.io/blog/)** that builds and manages Home Assistant, they work fast and humbly.
- **The horde of volunteer developers** of all components and add-ons.
- **The [vibrant community](https://community.home-assistant.io/)**, always willing to help and share code samples.
- **The [BRUH Automation](https://www.youtube.com/c/bruhautomation1) YouTube channel**, Ben's videos got me hooked on using Home Assistant.

Thank you for all your dedication, helpfulness and valuable insights. Cheers! :-)
