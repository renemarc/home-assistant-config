<h1 align="center">
  🏠<br/>Home Assistant configuration for a smart-looking place!<br/> <sup><sub>by <a href="https://renemarc.com/">René-Marc Simard</a> 😃</sub></sup>
</h1>

[![Price][badge-price]][link-license]
[![Home Assistant version][badge-ha-version]][link-ha-version]
[![Commits since last release][badge-commits]][link-commits]
[![GitHub Release][badge-release]][link-release]
[![Code Climate maintainability][badge-codeclimate-maintainability]][link-codeclimate-maintainability]
[![CodeFactor rating][badge-codefactor]][link-codefactor]
[![Build Status][badge-travis-ci]][link-travis-ci]
[![License][badge-license]][link-license]
[![Community Forum][badge-forum]][link-forum]
[![Tweet][badge-twitter]][link-twitter]

Configuration for [Home Assistant](https://www.home-assistant.io/) running on a [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) for a one bedroom apartment, offering convenience automations over lights and climate while providing multiple intuitive user controls.

<div align="center">
    <p><strong>Be sure to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> my repo if you find it useful! 😃</strong></p>
    <figure>
        <div>
            <img src="www/screenshots/dashboard-all.gif" alt="Dashboard animation" title="Dashboards">
        </div>
        <figcaption>
            <p><strong>Wall-mounted interface using <a href="/appdaemon/dashboards"><code>/appdaemon/dashboards/</code></a>.</strong></strong></p>
        </figcaption>
    </figure>
</div>

> **Note:** Images are from States UI days and still need to be updated in the documentation. This configuration now uses Lovelace UI and AppDaemon _exclusively_.

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-security-dark.png" alt="Security group (Dark theme)" title="Security (Dark theme)" width="200">
            <img src="www/screenshots/group-weather.png" alt="Weather group" title="Weather" width="200">
            <img src="www/screenshots/group-climate.png" alt="Climate Control group" title="Climate Control" width="200">
            <img src="www/screenshots/group-battery-dark.png" alt="Battery Levels group (Dark theme)" title="Battery Levels (Dark theme)" width="200">
            <img src="www/screenshots/group-atmosphere.png" alt="Atmospheric Safety group" title="Atmospheric Safety" width="200">
            <img src="www/screenshots/group-actions.png" alt="Actions group" title="Actions" width="200">
            <img src="www/screenshots/group-ceiling.png" alt="Ceiling group" title="Ceiling" width="200">
            <img src="www/screenshots/group-transit.png" alt="Public Transit group" title="Public Transit schedules" width="200">
        </div>
        <figcaption>
            <p><strong>Sensor <a href="groups"><code>/misc/groups.yaml</code></a>.</strong></p>
        </figcaption>
    </figure>
</div>

## Table of contents 📑

1. **[TL;DR](#tldr-)**
2. **[Overview](#overview-)**\
    [Goals](#goals-) | [Agile development](#agile-development-)
3. **[Key features](#key-features-)**\
    [Climate control](#climate-control-) | [Weather report](#weather-report-) | [Lighting control](#lighting-control-) | [Presence and basic security](#presence-and-basic-security-) | [Modes and scenes](#modes-and-scenes-) | [General information](#general-information-) | [Additional human interfaces](#additional-human-interfaces-)
4. **[Setup](#setup-)**\
    [Supporting hardware choices](#supporting-hardware-choices-) | [Configuration](#configuration-) | [Systems and bridges](#systems-and-bridges-) | [Physical devices](#physical-devices-) | [Software](#software-) | [Usage](#usage-)
5. **[License](#license-)**
6. **[Thanks](#thanks-)**

## TL;DR 🏃

This is a fully documented working configuration for Home Assistant, with screenshots, hints and comments. [Browse the code](#) to have a look! 👀

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Overview 🌅

### Goals ⚽

- **Inconspicuous**: I love tech alright, but like any good butlers it should stay out of sight yet stay summonable. Think Fiji villa, not server room.
- **Modular**: Both code and devices should be easily replaceable.
- **Internet independent**: As much local processing as possible for the essential features.
- **Accessible through multiple ways:** Computers, tablet (kiosk), voice, smart phones, wireless buttons, remotes.
- **Intuitive user interfaces:** One look at a group of sensors/switches should be sufficient for anyone to understand the current states and how to operate an interface. 💡
- **Redundant controls:** Multiple interfaces should be able to control devices without interference. State changes from manual interventions or dedicated manufacturer apps should be tracked whenever possible.
- **No information overload:** Provide just enough insights to get an idea of what's going on. And no need for data that's best consumed on more interactive devices (like stock prices, Steam community status…)
- **Not everything should be networked:** Bathroom fan, pantry and laundry room lights have their independent motion sensors and that's a good thing. Same independence goes for the smoke detector: I sure don't want to require extensive skin grafts because I forgot an extra space in a YAML file. 😱
- **No Alexa/Cortana/Google Voice:** I don't want to have advertising agencies, online stores, or other AI-feeding Big Brother tech-monsters listening in to everything we say _and do_ just for the dubious convenience of toggling lights by voice command. Privacy-centered, offline voice-control solutions like [Mycroft](https://mycroft.ai/blog/usability-vs-privacy-keeping-things-in-balance/), [Rhasspy](https://rhasspy.readthedocs.io/) look far more appealing.

<div align="center">
    <figure>
        <div>
            <a href="https://imgur.com/gallery/dlPPi" title="Wiretap meme"><img src="https://i.imgur.com/iVruWs1.jpg" alt="Wiretap meme" width="480"></a>
        </div>
        <figcaption>
            <p><strong>😨 No thanks!</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Agile development 🖖

This configuration is built with an [Agile](http://agilemanifesto.org/)-like methodology, lead by following main user stories:

- **As a resident** I want a reliable home automation platform to handle lights and climate that can easily be controlled and overridden in many intuitive ways.
- **As an apartment dweller** I want to have a discrete, non-permanent installation that takes as little space as possible.
- **As a developer** I want to use an open-source platform that is feature-rich, accessible, flexible and actively maintained.
- **As a consumer** I want to pick and choose which devices I wish to acquire without necessarily being locked into a closed ecosystem.
- **As a couple** we want to be able to operate lights and climate-control appliances as well as get quick overview of weather forecasts and public transit schedules through simple to use interfaces.

Tasks are hopefully defined in the [issue queue][link-issues] and their development progress is managed using a [lightweight Kanban board][link-board].

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=wujVMIYzYXg" title="Princess Bride clip"><img src="https://i.imgur.com/jKGbzWV.jpg" alt="Agile. You keep using that word. I do not think it means what you think it means." width="480"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=wujVMIYzYXg" title="Princess Bride clip">Well, without the sprints. And a team. And the retrospectives. And the…</a></strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Key features ✅

### Climate control 🌡

- **Temperature monitoring** averaged and rounded to compensate for sensor calibration issues.
- **Humidity monitoring** also averaged and rounded.
- **Low/High humidity status and alerts** in case something is wrong with the humidifier.
- **Mold conditions status and alert** in case someone transformed the place into a steam room.
- **Radon levels status and alert** to monitor the indoor concentration of this cancer-causing radioactive gas.

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-climate.png" alt="Climate Control group" title="Climate Control" width="325">
            <img src="www/screenshots/notification-humidity.png" alt="Humidity notification" title="Humidity notification" width="325">
        </div>
        <figcaption>
            <p><strong>Climate control.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Weather report ⛅

- **Easy to read status and forecasts** using [Dark Sky](https://darksky.net/) data and only showcasing parameters that actually matter, shown in obvious ways.
- **Outdoor air quality monitoring** with numeric levels and human-friendly categorization for ozone, carbon monoxide, nitrogen dioxide, sulphur dioxide, 2.5μm particulate matter and UV light, averaged from multiple surrounding public local stations.
- **Weather radar and satellite maps** for [local rain and snow](https://weather.gc.ca/radar/index_e.html) from Environment Canada and [regional air masses](http://www.nhc.noaa.gov/satellite.php) from the U.S. National Oceanic and Atmospheric Administration.
- See [`/misc/weather.yaml`](misc/weather.yaml) and [`/appdaemon/dashboards/`](appdaemon/dashboards).

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-weather.png" alt="Today's Weather group" title="Today's Weather" width="325">
            <img src="www/screenshots/group-forecast.png" alt="Weekly Forecast group" title="Weekly Forecast" width="325">
        </div>
        <figcaption>
            <p><strong>Today's weather and weekly forecast.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Lighting control 💡

- **Control for all pluggable lights**, smart ones at [`/lights/`](lights) and basic ones using [`/switches/`](switches).
- **Nanoleaf Aurora control**:
    - Manual theme selection.
    - Automatically rotate through device-based themes based on time of day (unless manually selected above).
- **LIFX Z bed underglow lights and ceiling wash lights control**:
    - Manual theme selection.
    - Automatically rotate through cloud-based themes based on time of day (unless manually selected above).
- **Automatically correlated colour temperature (CCT)** for [f.lux](https://justgetflux.com/)-like white temperature shift to gradually remove blue light based on a custom colour and brightness curve, not simply based on the sun …otherwise Canadian winters would be quite yellow!
- **Motion-based nightlights** where strategic lights fade in, dimmed very low, when movement is detected at night, say when someone wakes up to go the bathroom …again.
- See [`/lights/`](lights) and [`/automations/`](automations).

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-lounge.png" alt="Lounge group" title="Lounge lights" width="325">
            <img src="www/screenshots/group-bedroom.png" alt="Bedroom group" title="Bedroom lights" width="325">
        </div>
        <figcaption>
            <p><strong>Lighting controls.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Presence and basic security 👮

- **Cellphone device sensing** to check who is currently home or away.
- **Tamper monitoring** in case a perimeter device has been played with.
- **Water leak monitoring** to be able to react quickly when a pipe breaks.
- **Outdoor camera preview** to see who is at the door.
- **Opened door alert** to know if someone left an exteral door open.
- **Opened door indicators** where a chime is played and a few lights change colour briefly and subtly when the front door opens/closes, say to indicate an oblivious  showering partner that their better half has left or just came in.

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-presence.png" alt="Presence group" title="Presence" width="325">
            <img src="www/screenshots/group-security.png" alt="Security Status group" title="Security Status" width="325">
        </div>
        <figcaption>
            <p><strong>Presence and basic security.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Modes and scenes 🌈

- **Mode based** where unless a blocking mode is set, devices will turn on. Think of a river or a horse: tame it to keep it under control, but release the restraints and they will do their thing: 🐎
    - **Quiet mode** where noise makers know to stop or not to start.
    - **Nap time mode** that fades out lights in and near the bedroom and enables quiet mode.
    - **Night mode** fades out all lights outside of bedroom, enabling quiet mode too.
    - **Low-power mode** where each room knows which device should be on or off to achieve a more economical and calm state.
- **Smart rooms** that know which devices should be on or off based on the modes above. No need for heavy centralized control, let local managers handle their teams!
- **Good morning action** that releases all blocking modes, allowing all lights to turn on gradually, and noise-making devices are allowed to run if needed.
- **Smart global scenes** based on [`/scripts/`](scripts) instead of scenes, to allow for sequences and conditions:
    - **Movie scene** turns on ambiance lighting and dims smart lights when playing a movie, then returns to standard automations when pausing/stopping.
    - **Daylight/Gaming/Romantic global scenes** fade in and out different lights, select effects and change light colours to set a perfect mood.

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-actions.png" alt="Actions group" title="Actions" width="325">
        </div>
        <figcaption>
            <p><strong>Modes and scenes.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### General information 🛎

- **[Local bus schedules](https://www.home-assistant.io/integrations/gtfs)** with the next 3 departures. See [`/gtfs/`](gtfs) for optimization hints.
- **[Doomsday Clock](https://github.com/renemarc/home-assistant-doomsday-clock)** in case egocentric psychopaths keep on playing Russian roulette with humanity's future.
- **COVID-19 cases tracking** to estimate how prevalent this darn Coronavirus is locally and elsewhere on Earth.
- **Network status monitoring** for latency, upspeed, downspeed, monthly consumption, WiFi status…
- **Printer consumables monitoring** to estimate how many pages can be printed properly.
- **Home Assistant status monitoring** for geek cred with average load, RAM use, disk use, uptime, and update availability. 🤓
- **[Daily audio greeting](https://instaud.io/2Eye/?autoplay=1)** to start the day on a informed, uplifting note. See [`/automations/notifications/`](/automations/notifications).
- **GitHub repository monitoring** to track community health metrics for related repos.

<div align="center">
    <figure>
        <div>
            <img src="www/screenshots/group-system.png" alt="System group" title="System" width="325">
            <img src="www/screenshots/group-transit.png" alt="Public Transit group" title="Public Transit" width="325">
        </div>
        <figcaption>
            <p><strong>General information.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Additional human interfaces 📲

- **Aeotec Minimote** to quickly control global scenes and modes.
- **[Flic buttons](https://flic.io)** on a nightstand and in the kitchen for triggering modes and controlling localized lights, depending on current states and click types.
- **[HADashboard](https://www.home-assistant.io/docs/ecosystem/hadashboard/)** for wall-mounted tablet, featuring indoor sensors reports, transit schedules, weather forecast and radar/sattelite maps, wrapped in an obvious navigation scheme for much UX goodness. Have a look at [`/appdaemon/dashboards/`](appdaemon/dashboards), you'll like! 😍
- **[Home Assistant Companion](https://itunes.apple.com/us/app/home-assistant-companion/id1099568401?mt=8) iPhone app** for full UI access in the palm of my hand. _Muahahaha!_
- **[HomeKit](https://www.home-assistant.io/integrations/homekit/)** for using some key sensors and devices with iPhones.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Setup 🔩

<div align="center">
    <figure>
        <div>
            <img src="www/images/technology-diagram.png" alt="Home Assistant technology diagram">
        </div>
        <figcaption>
            <p><strong>Technology diagram (<a href="www/images/technology-diagram.png"><code>PNG</code></a>, <a href="www/images/technology-diagram.svg"><code>SVG</code></a>). Made with <a href="https://www.draw.io/?title=Home%20Assistant%20Technology%20Diagram.xml#Uhttps%3A%2F%2Fgithub.com%2Frenemarc%2Fhome-assistant-config%2Fraw%2Fmaster%2Fwww%2Fimages%2Ftechnology-diagram.xml">Draw.io</a> (<a href="www/images/technology-diagram.xml"><code>XML</code></a> source file).</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Supporting technical choices 🧱

- **Raspberry Pi 3B+** for it's compatibility, low-power, good-enough performance, and affordable price.
- **SSD via Sabrent USB adapter** to increase IO performance while reducing chances of disk corruption versus microSD cards.
- **Ubiquiti UniFi networking gear** because forking over some dough for reliable, rock-solid prosumer equipment makes everything run smoothly. And because hearing one less complaint (dropped WiFi signal) from the girlfriend is priceless. 🤕
- **Uninterruptible power supply** to ride over transient power failures.
- **WiFi** for its cheapness, omnipresence and non requirement of vendor-specific hubs.
- **Z-Wave** for reliability and guaranteed interoperability between vendors (unlike Zigbee…)

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Configuration ⚙

- **Dedicated, firewalled VLAN** (Virtual LAN) to segregate all IoT devices from other equipment …because I cannot trust that my vacuum cleaner won't go on a killing spree. Ever seen [_Runaway (1984)_](https://www.youtube.com/watch?v=zCZY9Z6WvSY) with Tom Selleck? Eek! 😱
- **Local static IPs** for all devices to minimize random drops.
- **Local development** on a local virtual machine using Python Virtual Env and Docker, then pulled with GIT on a Raspberry Pi.
- **Plentiful documentation** for my later self and to help out others.
- **Shareable code** with all identifiers kept in a non-committed, [`secrets.yaml`](./secrets-dummy.yaml) file.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Systems and bridges 🌉

| `Device` | `Description` | `Connection` |
|---------:|:--------------|:------------:|
| **[Aeotec Z-Stick Gen5](https://aeotec.com/z-wave-usb-stick)** | Z-Wave USB dongle. | USB
| **[Airthings Wave radon detector bridge](https://github.com/renemarc/balena-airthingswave)** | to interface with [this Bluetooth radon detector](https://airthings.com/wave/) by using [airthingswave-mqtt](https://github.com/hpeyerl/airthingswave-mqtt) from Herb Peyerl (**[@hpeyerl](https://github.com/hpeyerl)**). Runs on a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) managed through [balenaCloud](https://www.balena.io/cloud). | WiFi
| **[Blink Sync Module](https://blinkforhome.co.uk/products/blink-sync-module)** | for battery-operated, cloud-enabled cameras. | WiFi
| **[CEC MQTT bridge](https://github.com/michaelarnauts/cec-mqtt-bridge)** | to provide basic switching control and state sensing to a connected television. Runs on a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) managed through [balenaCloud](https://www.balena.io/cloud). | WiFi
| **[Flic smart button bridge](https://github.com/renemarc/balena-flic)** | to connect with [these Bluetooth Low Energy buttons](https://flic.io/). Runs on a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) managed through [balenaCloud](https://www.balena.io/cloud). | WiFi
| **[Milight iBox2 WiFi bridge](https://www.futlight.com/productdetails.aspx?id=239&typeid=125)** | for kitchen RF LED strip controllers, using [LimitlessLED](https://www.home-assistant.io/integrations/limitlessled) integration. | WiFi
| **[NooElec NESDR SMArt](http://www.nooelec.com/store/nesdr-smart.html)** | RTL-SDR (software-defined radio) USB dongle for reading AcuRite sensors. | USB
| **[Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)** | running Home Assistant. | Local

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Physical devices 🔨

#### LED lights 💡 (see [`/lights/`](./lights))

| `Device` | `Description` | `Connection` |
|---------:|:--------------|:------------:|
| **[24V 3014 Warm White Cool White LED Strip](http://ledmontreal.com/en/led-strips-without-accessories/24v-led-strips-without-accessories/cct-adjustable-led-strip.html)** | (x4) encased in custom-cut and assembled [light-diffusing aluminum profiles](http://ledmontreal.com/en/led-bars-and-profiles-led-montreal/continuous-lighting-aluminum-profile.html), connected to Milight RF controllers below. | Hardwire
| **[Adalight](https://learn.adafruit.com/adalight-diy-ambient-tv-lighting)** | DIY 100-dots TV backlighting controlled by [Lightpack+Prismatik](https://github.com/psieg/Lightpack) on HTPC. | LAN
| **DIY LED nightstand** | via TP-Link a smart plug. | WiFi
| **Fairy lights** | (x4) via TP-Link smart plugs. | WiFi
| **[LIFX Mini Color](https://www.lifx.com/products/lifx-mini-color)** | (x3) A19 RGBWW light bulbs. | WiFi
| **[LIFX+](https://www.lifx.com/products/lifx-plus)** | (x2) A19 RGBWW light bulbs with infrared. | WiFi
| **[LIFX Z](https://www.lifx.com/products/lifx-z-starter-kit-without-homekit)** | (x5) light strips (non-HomeKit versions) as bed underglow and ceiling wash lights. | WiFi
| **[Milight CCT LED RF Controller](https://www.futlight.com/productdetails.aspx?id=293&typeid=146)** | (x4) for white-adjustable undercabinet kitchen lights, connected to appropriate UL-listed power supplies. | 2.4Ghz
| **[Nanoleaf Aurora](https://nanoleaf.me)** | light panels kit. Pretty! | WiFi

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Sensors 📡 (see [`/sensors/`](./sensors))

| `Device` | `Usage` | `Connection` |
|---------:|:--------|:------------:|
| **[AcuRite 06044M Wireless Sensor](https://www.acurite.com/indoor-temperature-sensor-and-humidity-gauge.html)** | for cheap temperature and humidity monitoring inside a cigar humidor. | 433Mhz
| **[Aeotec Door / Window Sensor Gen5](https://aeotec.com/z-wave-door-window-sensor)** | for front door. | Z-Wave
| **[Aeotec MultiSensor 6](https://aeotec.com/z-wave-sensor)** | (x3) for temperature/humidity/presence detection. | Z-Wave
| **[Airthings Wave radon detector](https://airthings.com/wave/)** | to keep an eye on this cancer-causing radioactive gas. | Bluetooth Low Energy
| **[Blink XT2](https://blinkforhome.com/products)** | to keep a record of any movement outside. | WiFi / 900MHz
| **[Dome Leak Sensor](https://domeha.com/z-wave-leak-sensor)** | (x2) in case the dishwasher breaks a seal, a shower curtain has not been closed properly …or a toilet has overflowed. 🤢 | Z-Wave
| **[Ecolink Firefighter](https://products.z-wavealliance.org/products/1827)** | to warn those outside that the fire alarm has been triggered. | Z-Wave

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Human interfaces 🕹️

| `Device` | `Description` | `Connection` |
|---------:|:--------------|:------------:|
| **[Acer Iconia One 10" tablet](https://www.acer.com/ac/en/CA/content/series/iconiaone10)** | with its 1280x800 IPS screen wallmounted as a kiosk. See [`/appdaemon/dashboards/`](appdaemon/dashboards). | WiFi
| **[Aeotec Minimote](https://www.youtube.com/watch?v=5Vc1Ift7ND8)** | with its 4 double-state remote control buttons. | Z-Wave
| **[Flic Smart Buttons](https://flic.io)** | (x2) for simple, triple-state, stick-anywhere, battery-powered physical buttons. 🔘 | Bluetooth Low Energy

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Switches and other devices 🔌

| `Device` | `Usage` | `Connection` |
|---------:|:--------|:------------:|
| **[Daikin 19 Series mini split heat pump](https://daikincomfort.com/products/heating-cooling/single-zone/heat-pumps/wall-mount-19-series-heat-pump)** | to cool, warm, and dehumidify the apartment. Connected via the [optional WiFi adapter](http://www.daikinac.com/content/residential/residential-controllers/daikin-comfort-control-app/) or [Broadlink RM Mini 3](https://www.ibroadlink.com/rmMini3/) _(upcoming)_. | IR / WiFi
| **[Rowenta VU2660U2 Turbo Silence Extreme oscillating fan](https://www.rowenta.ca/en/Home-Comfort/Fans/Turbo-Silence-12%E2%80%9D-Table-Fan/p/1830006169)** | to create a gentle, silent breeze in the bedroom. Connected via [Broadlink RM Mini 3](https://www.ibroadlink.com/rmMini3/) _(upcoming)_. | IR
| **[TP-Link HS105 Smart Plugs](http://www.tp-link.com/us/products/details/cat-5516_HS105.html)** | (x4) to toggle power to dumb devices. | WiFi

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Software 💻

| `App` | `Usage` |
|------:|:--------|
| **[Docker](https://www.docker.com)** | on local machine (for development). True, Home Assistant is Docker-based too… 😉
| **[Fully Kiosk Browser PLUS](https://www.ozerov.de/fully-kiosk-browser/)** | on wallmounted tablet for display and simple interaction.
| **[Home Assistant](https://www.home-assistant.io/)** | on a Raspberry Pi 3 Model B+ (production setup).
| **[LANnouncer](http://www.keybounce.com/lannouncer/)** | on wallmounted tablet for simple audio and text-to-speech messaging. Quite unreliable however.
| **[Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html)** | on local machine (for quick development).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Home Assistant add-ons ➕

| `Add-on` | `Usage` |
|---------:|:--------|
| **[AppDaemon](https://github.com/home-assistant/appdaemon)** | for [HADashboard](https://www.home-assistant.io/docs/ecosystem/hadashboard/) tablet UI.
| **[Check Home Assistant configuration](https://github.com/home-assistant/hassio-addons/tree/master/check_config)** | to validate current configuration before upgrading.
| **[DuckDNS](https://github.com/home-assistant/hassio-addons/tree/master/duckdns)** | to facilitate secure remote access.
| **[Log Viewer](https://github.com/hassio-addons/addon-log-viewer)** | to stream the log file to a browser window.
| **[MQTT Server & Web client](https://github.com/hassio-addons/addon-mqtt)** | for standard IoT messaging using [Mosquitto](https://mosquitto.org/), plus a [HiveMQ](https://www.hivemq.com/) web interface.
| **[NGINX Home Assistant SSL proxy](https://github.com/home-assistant/hassio-addons/tree/master/nginx_proxy)** | to route secured web traffic from the outside world to Home Assistant using [NGINX](https://www.nginx.com/).
| **[RTL_433 to MQTT Bridge](https://github.com/james-fry/hassio-addons)** | to receive and decode AcuRite devices radio signals.
| **[Samba share](https://github.com/home-assistant/hassio-addons/tree/master/samba)** | to access configuration files easily with [Samba](https://www.samba.org/).
| **[SSH & Web Terminal](https://github.com/hassio-addons/addon-ssh)** | for secure command-line access.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Community integrations 🏘️

| `Integration` | `Usage` |
|--------------:|:--------|
| **[Browser Mod](https://github.com/thomasloven/hass-browser_mod)** | to add pop-up support to [`ui-lovelace.yaml`](./ui-lovelace.yaml).
| **[Display platform](https://github.com/daemondazz/homeassistant-displays)** | for integration with the [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/).
| **[Doomsday Clock](https://github.com/renemarc/home-assistant-doomsday-clock)** | to [track how close](https://thebulletin.org/doomsday-clock/current-time/) humanity is to a man-made global catastrophe.
| **[HACS (Home Assistant Commnunity Store)](https://hacs.xyz/)** | to ease maintenance and pretty-up [`ui-lovelace.yaml`](./ui-lovelace.yaml).
| **[Lightpack](https://github.com/kklemm91/Lightpack-HASS)** | to control TV bias lights.
| **[Raspberry Pi Power Supply Checker](https://github.com/custom-components/sensor.rpi_power)** | to warn in case of insufficient power delivery.
| **[UniFi Gateway](https://github.com/custom-components/sensor.unifigateway)** | for extra network stats.
| **[Variable](https://github.com/rogro82/hass-variables)** | for persisnent storage of non-boolean values.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

#### Lovelace widgets 💖

| `Widget` | `Usage` |
|---------:|:--------|
| **[auto-entities](https://github.com/thomasloven/lovelace-auto-entities)** | to filter entities.
| **[bar-card](https://github.com/custom-cards/bar-card)** | for battery statuses.
| **[button card](https://github.com/custom-cards/button-card)** | for intuitive mode toggles.
| **[card-mod](https://github.com/thomasloven/lovelace-card-mod)** | to apply CSS to cards.
| **[card-tools](https://github.com/thomasloven/lovelace-card-tools)** | as a requirement to other widgets.
| **[custom-header](https://github.com/maykar/custom-header)** | to optimize screen real-estate.
| **[dummy-entity-row](https://github.com/thomasloven/lovelace-dummy-entity-row)** | to use entities' titles without showing their values.
| **[favicon-counter](https://github.com/custom-cards/favicon-counter)** | to display a browser tab indicator for notifications.
| **[fold-entity-row](https://github.com/thomasloven/lovelace-fold-entity-row)** | to hide less important details unless requested.
| **[github-entity-row](https://github.com/benct/lovelace-github-entity-row)** | to display health status of related GitHub repos.
| **[layout-card](https://github.com/thomasloven/lovelace-layout-card)** | to give structure to views, including pretty headers and footers.
| **[mini-graph-card](https://github.com/kalkih/mini-graph-card)** | to display simple interactive line charts for temperature, humidity, radon levels…
| **[restriction-card](https://github.com/iantrich/restriction-card)** | to prevent accidental changes to critical entities.
| **[secondaryinfo-entity-row](https://github.com/custom-cards/secondaryinfo-entity-row)** | to display supplemental information from other sensors and attributes.
| **[slider-entity-row](https://github.com/thomasloven/lovelace-slider-entity-row)** | to quikly control light brightness.
| **[swipe-card](https://github.com/bramkragten/custom-ui/tree/master/swipe-card)** | to display slideshows of satellite weather maps.
| **[vertical-stack-in-card](https://github.com/custom-cards/vertical-stack-in-card)** | to assemble multiple sub-cards into a prettier, unified card.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### Usage 📘

In an empty directory, type:

```shell
git clone --recurse-submodules git@github.com:renemarc/home-assistant-config.git .

echo "secrets.yaml filter=secret merge=keepMine" > .gitattributes

cp secrets-dummy.yaml secrets.yaml

cp appdaemon/secrets-dummy.yaml appdaemon/secrets.yaml
```

Actual secrets and auto-generated sensitive files are obviously kept off this repo! 😉

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## License 📃

- Code and configuration is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
- Documentation is licensed under the Creative Commons [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Thanks 💕

Kudos to:

- **The [dedicated core team](https://www.home-assistant.io/blog)** that builds and manages Home Assistant. They work fast and humbly.
- **The horde of volunteer developers** of all components and add-ons.
- **The [vibrant community](https://community.home-assistant.io)**, always willing to help and share code samples.
- **The [BRUH Automation](https://www.youtube.com/c/bruhautomation1) YouTube channel**, Ben's videos got me hooked on using Home Assistant.

Thank you for all your dedication, helpfulness and valuable insights. Cheers! 🍻😃

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> or <a href="#" title="fork">🔱</a> this repo! 😃</strong></p>

[badge-codeclimate-maintainability]:https://img.shields.io/codeclimate/maintainability/renemarc/home-assistant-config.svg?logo=code-climate&cacheSeconds=300

[badge-codefactor]:https://img.shields.io/codefactor/grade/github/renemarc/home-assistant-config?logo=codefactor&logoColor=white&cacheSeconds=300

[badge-commits]:https://img.shields.io/github/commits-since/renemarc/home-assistant-config/latest/master.svg?label=commits%20since%20last%20release&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij4KCTxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xMy41LDhIMTJWMTNMMTYuMjgsMTUuNTRMMTcsMTQuMzNMMTMuNSwxMi4yNVY4TTEzLDNBOSw5IDAgMCwwIDQsMTJIMUw0Ljk2LDE2LjAzTDksMTJINkE3LDcgMCAwLDEgMTMsNUE3LDcgMCAwLDEgMjAsMTJBNyw3IDAgMCwxIDEzLDE5QzExLjA3LDE5IDkuMzIsMTguMjEgOC4wNiwxNi45NEw2LjY0LDE4LjM2QzguMjcsMjAgMTAuNSwyMSAxMywyMUE5LDkgMCAwLDAgMjIsMTJBOSw5IDAgMCwwIDEzLDMiIC8+Cjwvc3ZnPgo=&cacheSeconds=300

[badge-forum]:https://img.shields.io/badge/community-forum-brightgreen.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xNywxMlYzQTEsMSAwIDAsMCAxNiwySDNBMSwxIDAgMCwwIDIsM1YxN0w2LDEzSDE2QTEsMSAwIDAsMCAxNywxMk0yMSw2SDE5VjE1SDZWMTdBMSwxIDAgMCwwIDcsMThIMThMMjIsMjJWN0ExLDEgMCAwLDAgMjEsNloiIC8+Cjwvc3ZnPg==&maxAge=86400

[badge-ha-version]:https://img.shields.io/badge/works_with-Home_Assistant_0.108.8-53c1f1.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTIxLjgsMTNIMjBWMjFIMTNWMTcuNjdMMTUuNzksMTQuODhMMTYuNSwxNUMxNy42NiwxNSAxOC42LDE0LjA2IDE4LjYsMTIuOUMxOC42LDExLjc0IDE3LjY2LDEwLjggMTYuNSwxMC44QTIuMSwyLjEgMCAwLDAgMTQuNCwxMi45TDE0LjUsMTMuNjFMMTMsMTUuMTNWOS42NUMxMy42Niw5LjI5IDE0LjEsOC42IDE0LjEsNy44QTIuMSwyLjEgMCAwLDAgMTIsNS43QTIuMSwyLjEgMCAwLDAgOS45LDcuOEM5LjksOC42IDEwLjM0LDkuMjkgMTEsOS42NVYxNS4xM0w5LjUsMTMuNjFMOS42LDEyLjlBMi4xLDIuMSAwIDAsMCA3LjUsMTAuOEEyLjEsMi4xIDAgMCwwIDUuNCwxMi45QTIuMSwyLjEgMCAwLDAgNy41LDE1TDguMjEsMTQuODhMMTEsMTcuNjdWMjFINFYxM0gyLjI1QzEuODMsMTMgMS40MiwxMyAxLjQyLDEyLjc5QzEuNDMsMTIuNTcgMS44NSwxMi4xNSAyLjI4LDExLjcyTDExLDNDMTEuMzMsMi42NyAxMS42NywyLjMzIDEyLDIuMzNDMTIuMzMsMi4zMyAxMi42NywyLjY3IDEzLDNMMTcsN1Y2SDE5VjlMMjEuNzgsMTEuNzhDMjIuMTgsMTIuMTggMjIuNTksMTIuNTkgMjIuNiwxMi44QzIyLjYsMTMgMjIuMiwxMyAyMS44LDEzTTcuNSwxMkEwLjksMC45IDAgMCwxIDguNCwxMi45QTAuOSwwLjkgMCAwLDEgNy41LDEzLjhBMC45LDAuOSAwIDAsMSA2LjYsMTIuOUEwLjksMC45IDAgMCwxIDcuNSwxMk0xNi41LDEyQzE3LDEyIDE3LjQsMTIuNCAxNy40LDEyLjlDMTcuNCwxMy40IDE3LDEzLjggMTYuNSwxMy44QTAuOSwwLjkgMCAwLDEgMTUuNiwxMi45QTAuOSwwLjkgMCAwLDEgMTYuNSwxMk0xMiw2LjlDMTIuNSw2LjkgMTIuOSw3LjMgMTIuOSw3LjhDMTIuOSw4LjMgMTIuNSw4LjcgMTIsOC43QzExLjUsOC43IDExLjEsOC4zIDExLjEsNy44QzExLjEsNy4zIDExLjUsNi45IDEyLDYuOVoiIGZpbGw9IiNmZmZmZmYiIC8+PC9zdmc+Cg==&maxAge=21600

[badge-license]:https://img.shields.io/github/license/renemarc/home-assistant-config.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTE3LjgsMjBDMTcuNCwyMS4yIDE2LjMsMjIgMTUsMjJINUMzLjMsMjIgMiwyMC43IDIsMTlWMThINUwxNC4yLDE4QzE0LjYsMTkuMiAxNS43LDIwIDE3LDIwSDE3LjhNMTksMkMyMC43LDIgMjIsMy4zIDIyLDVWNkgyMFY1QzIwLDQuNCAxOS42LDQgMTksNEMxOC40LDQgMTgsNC40IDE4LDVWMThIMTdDMTYuNCwxOCAxNiwxNy42IDE2LDE3VjE2SDVWNUM1LDMuMyA2LjMsMiA4LDJIMTlNOCw2VjhIMTVWNkg4TTgsMTBWMTJIMTRWMTBIOFoiIGZpbGw9IiNmZmZmZmYiIC8+PC9zdmc+Cg==&maxAge=86400

[badge-price]:https://img.shields.io/badge/price-FREE-53c1f1.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTcsMTVIOUM5LDE2LjA4IDEwLjM3LDE3IDEyLDE3QzEzLjYzLDE3IDE1LDE2LjA4IDE1LDE1QzE1LDEzLjkgMTMuOTYsMTMuNSAxMS43NiwxMi45N0M5LjY0LDEyLjQ0IDcsMTEuNzggNyw5QzcsNy4yMSA4LjQ3LDUuNjkgMTAuNSw1LjE4VjNIMTMuNVY1LjE4QzE1LjUzLDUuNjkgMTcsNy4yMSAxNyw5SDE1QzE1LDcuOTIgMTMuNjMsNyAxMiw3QzEwLjM3LDcgOSw3LjkyIDksOUM5LDEwLjEgMTAuMDQsMTAuNSAxMi4yNCwxMS4wM0MxNC4zNiwxMS41NiAxNywxMi4yMiAxNywxNUMxNywxNi43OSAxNS41MywxOC4zMSAxMy41LDE4LjgyVjIxSDEwLjVWMTguODJDOC40NywxOC4zMSA3LDE2Ljc5IDcsMTVaIiBmaWxsPSIjZmZmIiAvPjwvc3ZnPgo=&maxAge=86400

[badge-release]:https://img.shields.io/github/release/renemarc/home-assistant-config/all.svg?logo=git&logoColor=white&maxAge=21600

[badge-travis-ci]:https://img.shields.io/travis/renemarc/home-assistant-config.svg?logo=travis-ci&logoColor=White

[badge-twitter]:https://img.shields.io/twitter/url/http/shields.io.svg?style=social&maxAge=86400

[link-board]:https://github.com/renemarc/home-assistant-config/projects/1
[link-codeclimate-maintainability]:https://codeclimate.com/github/renemarc/home-assistant-config
[link-codefactor]:https://www.codefactor.io/repository/github/renemarc/home-assistant-config
[link-commits]:https://github.com/renemarc/home-assistant-config/compare/v2018.12.18...master
[link-forum]:https://community.home-assistant.io/t/wall-mounted-dashboard-with-fully-documented-repo/57989
[link-ha-version]:https://github.com/home-assistant/home-assistant/tree/0.108.8
[link-issues]:https://github.com/renemarc/home-assistant-config/issues
[link-license]:LICENSE.txt
[link-release]:https://github.com/renemarc/home-assistant-config/releases
[link-travis-ci]:https://travis-ci.org/renemarc/home-assistant-config
[link-twitter]:https://twitter.com/intent/tweet?text=Automate%20your%20home%20into%20a%20smart-looking%20place!&url=https://github.com/renemarc/home-assistant-config&via=renemarc&hashtags=HomeAssistant,SmartHome,ConnectedHome,HomeAutomation,IoT
