# RTL433 to MQTT Bridge hass.io addon

These are the customizable scripts for the [RTL433 to MQTT Bridge hass.io addon](https://github.com/james-fry/hassio-addons/tree/master/rtl4332mqtt).

## Scripts

### [`📡 ./rtl2mqtt.sh`](rtl2mqtt.sh)

This is the main entry point for the Docker container. It is currently set to respond to only one protocol for [AcuRite's 592TXR Temp/Humidity sensor](https://www.acurite.com/indoor-temperature-sensor-and-humidity-gauge.html), therefore it would need to be modified should more than one device type need to be handled.
