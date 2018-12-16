<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **switches** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#switches" title="Switches
(Scene from the movie Modern Times)"><img src="https://media.giphy.com/media/6IcwJKMNlDDCU/giphy.gif" alt="Factory boss playing with switches in Modern Times" width="400"></a>
    </div>
</figure>

<h1 align="center">Switches</h1>

## TP-Link HS105 smart Wi-Fi plug mini outlets

A few [TP-Link smart plug mini outlets](http://www.tp-link.com/us/products/details/cat-5516_HS105.html) are used to control dumb devices.

They were first setup with the manufaturer's [Kasa app](https://www.tp-link.com/us/home-networking/smart-home/kasa.html). Then they were assigned static IP addresses in my router to avoid occasional drops due to DHCP renewal limbo.

Still, some of them tend to drop off randomly if placed behind furniture or close to other wi-fi outlets/devices. I am considering moving to Zwave outlets or smart plugs to increase the reliabilty.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Aeotec Z-Stick blinking light

[Aeotec Z-Stick disco light](https://community.home-assistant.io/t/aeotec-gen5-z-stick-strobing-led-question-in-hass-io/28635/9) command line switch to enable or disable the USB dongle's LED light.

The [Z-Stick Zwave Gen5](https://aeotec.com/z-wave-usb-stick) USB dongle has a colourful but annoying blinking status LED. Great for diagnosis, but otherwise very bright and obnoxious when placed in a visible location!

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## HDMI-CEC TV switch

This switch allows basic MQTT status and control of televisions using [this HDMI-CEC to MQTT bridge](https://github.com/michaelarnauts/cec-mqtt-bridge) by **@michaelarnauts** that talks to the Mosquitto MQTT add-on. Using the [CEC protocol](https://en.wikipedia.org/wiki/Consumer_Electronics_Control), the connected television can then have its power state known and toggled through the UI, Apple HomeKit, and most importantly in automations.

The bridge is hosted on a inexpensive, dedicated, Wi-Fi enabled [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) connected to a free HDMI port on the lounge's television. Contrary to most video cards, all Raspberry Pi models fully support the HDMI-CEC prototol.

The quickest route would have been to simply install the code directly on a full-blown Raspbian installation, but that leads to possible file system corruption during ungraceful shutdowns (pulled plug, power outages), SD card degradation due to regular disk writes, the need for security management, eventual OS upgrade cycles and other manual maintenance. All that for a simple TV switch? No thanks.

Instead, this RPi is running [balenaOS](https://www.balena.io/os/) (like Hass.io did before moving on to their own HassOS) to create an Docker-powered plug-in appliance thanks to its read-only root file system and non-persistent RAM logging that minimize chances of SD card corruption.

[Initial deployment was done locally](https://www.balena.io/docs/learn/develop/local-mode/) using a [development OS image of balenaOS](https://www.balena.io/docs/reference/OS/overview/2.x/#dev-vs-prod-images) (password-less SSH access, exposed Docker socket) to make sure everything worked fine. Then I rebuilt the device using a production image to secure most access points to the device except for secured CLI and remote management using balenaCloud's [free-tier](https://www.balena.io/pricing/) control panel service. This way there is little maintenance to do, except click-deploying OS updates whenever security or performance updates are available. And if I add more TVs later, it's just as simple to manage many such IoT devices as it is to manage one. A bit like when updating firmware for other smart devices. Easy! 😃

### Local/Test installation

With the base balenaOS running on the RPi, and with the [balena-cli installed](https://www.balena.io/docs/reference/cli/):

```shell
git clone git@github.com:michaelarnauts/cec-mqtt-bridge.git
cd cec-mqtt-bridge
cp config.default.ini config.ini
```

Then edit the `config.ini` file with your MQTT details.

Finally, create the Docker container and push the app to the device (assuming here that hostname is named **balena.local**):

```shell
sudo balena local push balena.local --source .
```

To test communication or debug CEC codes, connect to the app container using:

```shell
sudo balena local ssh balena.local
```

First, list the CEC-enabled devices using:

```shell
echo "scan" | cec-client RPI -s -d 1
```

Then simply listen to the CEC bus while using your remote control or while testing your integration:

```shell
cec-client RPI -s -d 31
```

See [Gordon Turner's blog post](https://blog.gordonturner.com/2016/12/14/using-cec-client-on-a-raspberry-pi/) for more information, and use [CEC-O-MATIC](http://www.cec-o-matic.com/) to decypher those obscure `10:47:43:45:43:54:65:73:74:65:72` CEC messages and generate your own replies.

### Production installation

As of this writing, a development build cannot yet be promoted into a production build, so if everything is working well in test let's rebuild things in production.

First, create a Raspberry Pi app on the [balenaCloud dashboard](https://dashboard.balena-cloud.com/) corresponging to your model.

Then, add a device to your app in the balenaCloud dashboard, selecting **Production** edition. You can either configure WiFi here first or manually configure it on the resulting image by using:

```shell
sudo balena local configure ~/Downloads/balena-APPNAME-raspberry-pi-VERSION.img
```

Once burned to an SD card and the Raspberry Pi booted up, it will be listed on your dashboard.

Ideally, instead of relying on a configuration file, setup environment variables for any or all of the following. This way, should you have more than one device you can setup fleet-wide configuration values and some device-specific ones, without having to rebuild the app.

```ini
MQTT_BROKER
MQTT_PORT
MQTT_USER
MQTT_PASSWORD
MQTT_PREFIX
CEC_ENABLED
CEC_ID
CEC_PORT
CEC_DEVICES
IR_ENABLED
```

Then, add balenaCloud as a remote to the Git project:

```shell
git remote add balena USERNAME@git.balena-cloud.com::USERNAME/APPNAME.git
```

Push the codebase directory (including configuration file) to the balenaCloud build pipeline, deploying it to your Raspberry Pi.

```shell
balena push APPNAME
```

Later, should you add another TV, simply add another device to this application and override some environment variables like MQTT_PREFIX for this specific device. The new device will then automatically be provisioned and ready to go!

### Tweaks

You can tweak your application in the dashboard and [override boot settings](https://www.balena.io/docs/reference/OS/advanced/), for instance so that the CEC-to-MQTT bridge doesn't switch the TV to the balenaOS blank screen when booting up by adding:

```ini
RESIN_HOST_CONFIG_hdmi_ignore_cec_init=1
```

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Customization

Some customization of switches is done in [`/customize.yaml`](../customize.yaml). For privacy as well as for development and testing purposes any sensitive data is hidden and referenced in the non-commited [`/secrets.yaml`](../secrets-dummy.yaml) file.

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
