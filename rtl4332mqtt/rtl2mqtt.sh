#!/bin/sh

# A simple script that will receive events from an RTL433 SDR and resend the data via MQTT

# Author: Chris Kacerguis <chriskacerguis@gmail.com>
# Modification for hass.io add-on: James Fry

# Below are rtl_433 options and the supported device protocols as of 25/10/2017
# **NOTE that the protocol number is NOT persistent and seems to change**
# Hence always verify protocol numbers in logs when starting the add-on
# The key arguments required are:
# -F json  --> this sets JSON formatted output for easier MQTT
# -R <protocol number>  --> this tells rtl_433 which protocol(s) to scan for

# Usage:  = Tuner options =
#         [-d <RTL-SDR USB device index>] (default: 0)
#         [-g <gain>] (default: 0 for auto)
#         [-f <frequency>] [-f...] Receive frequency(s) (default: 433920000 Hz)
#         [-H <seconds>] Hop interval for polling of multiple frequencies (default: 600 seconds)
#         [-p <ppm_error] Correct rtl-sdr tuner frequency offset error (default: 0)
#         [-s <sample rate>] Set sample rate (default: 250000 Hz)
#         [-S] Force sync output (default: async)
#         = Demodulator options =
#         [-R <device>] Enable only the specified device decoding protocol (can be used multiple times)
#         [-G] Enable all device protocols, included those disabled by default
#         [-l <level>] Change detection level used to determine pulses [0-16384] (0 = auto) (default: 0)
#         [-z <value>] Override short value in data decoder
#         [-x <value>] Override long value in data decoder
#         [-n <value>] Specify number of samples to take (each sample is 2 bytes: 1 each of I & Q)
#         = Analyze/Debug options =
#         [-a] Analyze mode. Print a textual description of the signal. Disables decoding
#         [-A] Pulse Analyzer. Enable pulse analyzis and decode attempt
#         [-I] Include only: 0 = all (default), 1 = unknown devices, 2 = known devices
#         [-D] Print debug info on event (repeat for more info)
#         [-q] Quiet mode, suppress non-data messages
#         [-W] Overwrite mode, disable checks to prevent files from being overwritten
#         [-y <code>] Verify decoding of demodulated test data (e.g. "{25}fb2dd58") with enabled devices
#         = File I/O options =
#         [-t] Test signal auto save. Use it together with analyze mode (-a -t). Creates one file per signal
#                  Note: Saves raw I/Q samples (uint8 pcm, 2 channel). Preferred mode for generating test files
#         [-r <filename>] Read data from input file instead of a receiver
#         [-m <mode>] Data file mode for input / output file (default: 0)
#                  0 = Raw I/Q samples (uint8, 2 channel)
#                  1 = AM demodulated samples (int16 pcm, 1 channel)
#                  2 = FM demodulated samples (int16) (experimental)
#                  3 = Raw I/Q samples (cf32, 2 channel)
#                  Note: If output file is specified, input will always be I/Q
#         [-F] kv|json|csv Produce decoded output in given format. Not yet supported by all drivers.
#                 append output to file with :<filename> (e.g. -F csv:log.csv), defaults to stdout.
#         [-C] native|si|customary Convert units in decoded output.
#         [-T] specify number of seconds to run
#         [-U] Print timestamps in UTC (this may also be accomplished by invocation with TZ environment variable set).
#         [<filename>] Save data stream to output file (a '-' dumps samples to stdout)
#
# Supported device protocols:
#     [01]* Silvercrest Remote Control
#     [02]  Rubicson Temperature Sensor
#     [03]  Prologue Temperature Sensor
#     [04]  Waveman Switch Transmitter
#     [05]* Steffen Switch Transmitter
#     [06]* ELV EM 1000
#     [07]* ELV WS 2000
#     [08]  LaCrosse TX Temperature / Humidity Sensor
#     [09]* Template decoder
#     [10]* Acurite 896 Rain Gauge
#     [11]  Acurite 609TXC Temperature and Humidity Sensor
#     [12]  Oregon Scientific Weather Sensor
#     [13]  Mebus 433
#     [14]* Intertechno 433
#     [15]  KlikAanKlikUit Wireless Switch
#     [16]  AlectoV1 Weather Sensor (Alecto WS3500 WS4500 Ventus W155/W044 Oregon)
#     [17]  Cardin S466-TX2
#     [18]  Fine Offset Electronics, WH2 Temperature/Humidity Sensor
#     [19]  Nexus Temperature & Humidity Sensor
#     [20]  Ambient Weather Temperature Sensor
#     [21]  Calibeur RF-104 Sensor
#     [22]* X10 RF
#     [23]* DSC Security Contact
#     [24]* Brennenstuhl RCS 2044
#     [25]  GT-WT-02 Sensor
#     [26]  Danfoss CFR Thermostat
#     [27]* Energy Count 3000 (868.3 MHz)
#     [28]* Valeo Car Key
#     [29]  Chuango Security Technology
#     [30]  Generic Remote SC226x EV1527
#     [31]  TFA-Twin-Plus-30.3049 and Ea2 BL999
#     [32]  Fine Offset Electronics WH1080/WH3080 Weather Station
#     [33]  WT450
#     [34]  LaCrosse WS-2310 Weather Station
#     [35]  Esperanza EWS
#     [36]  Efergy e2 classic
#     [37]* Inovalley kw9015b, TFA Dostmann 30.3161 (Rain and temperature sensor)
#     [38]  Generic temperature sensor 1
#     [39]  WG-PB12V1
#     [40]* Acurite 592TXR Temp/Humidity, 5n1 Weather Station, 6045 Lightning
#     [41]* Acurite 986 Refrigerator / Freezer Thermometer
#     [42]  HIDEKI TS04 Temperature, Humidity, Wind and Rain Sensor
#     [43]  Watchman Sonic / Apollo Ultrasonic / Beckett Rocket oil tank monitor
#     [44]  CurrentCost Current Sensor
#     [45]  emonTx OpenEnergyMonitor
#     [46]  HT680 Remote control
#     [47]  S3318P Temperature & Humidity Sensor
#     [48]  Akhan 100F14 remote keyless entry
#     [49]  Quhwa
#     [50]  OSv1 Temperature Sensor
#     [51]  Proove
#     [52]  Bresser Thermo-/Hygro-Sensor 3CH
#     [53]  Springfield Temperature and Soil Moisture
#     [54]  Oregon Scientific SL109H Remote Thermal Hygro Sensor
#     [55]  Acurite 606TX Temperature Sensor
#     [56]  TFA pool temperature sensor
#     [57]  Kedsum Temperature & Humidity Sensor
#     [58]  blyss DC5-UK-WH (433.92 MHz)
#     [59]  Steelmate TPMS
#     [60]  Schrader TPMS
#     [61]* LightwaveRF
#     [62]  Elro DB286A Doorbell
#     [63]  Efergy Optical
#     [64]  Honda Car Key
#     [65]* Template decoder
#     [66]  Fine Offset Electronics, XC0400
#     [67]  Radiohead ASK
#     [68]  Kerui PIR Sensor
#     [69]  Fine Offset WH1050 Weather Station
#     [70]  Honeywell Door/Window Sensor
#     [71]  Maverick ET-732/733 BBQ Sensor
#     [72]* RF-tech
#     [73]  LaCrosse TX141TH-Bv2 sensor
#     [74]  Acurite 00275rm,00276rm Temp/Humidity with optional probe
#     [75]  LaCrosse TX35DTH-IT Temperature sensor
#     [76]  LaCrosse TX29IT Temperature sensor
#     [77]  Vaillant calorMatic 340f Central Heating Control
#     [78]  Fine Offset Electronics, WH25 Temperature/Humidity/Pressure Sensor
#     [79]  Fine Offset Electronics, WH0530 Temperature/Rain Sensor
#     [80]  IBIS beacon
#     [81]  Oil Ultrasonic STANDARD FSK
#     [82]  Citroen TPMS
#     [83]  Oil Ultrasonic STANDARD ASK
#     [84]  Thermopro TP11 Thermometer
#     [85]  Solight TE44
#     [86]  Wireless Smoke and Heat Detector GS 558
#     [87]  Generic wireless motion sensor
#     [88]  Toyota TPMS
#     [89]  Ford TPMS
#     [90]  Renault TPMS
#     [91]* inFactory
#     [92]  FT-004-B Temperature Sensor
#     [93]  Ford Car Key
#     [94]  Philips outdoor temperature sensor
#     [95]  Schrader TPMS EG53MA4
#     [96]  Nexa
#     [97]  Thermopro TP12 Thermometer
#     [98]  GE Color Effects
#     [99]  X10 Security
#    [100]  Interlogix GE UTC Security Devices
#    [101]* Dish remote 6.3
#
# * Disabled by default, use -R n or -G

export LANG=C
PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

CONFIG_PATH=/data/options.json
MQTT_HOST="$(jq --raw-output '.mqtt_host' $CONFIG_PATH)"
MQTT_PORT="1883"
MQTT_USER="$(jq --raw-output '.mqtt_user' $CONFIG_PATH)"
MQTT_PASS="$(jq --raw-output '.mqtt_password' $CONFIG_PATH)"
MQTT_TOPIC="$(jq --raw-output '.mqtt_topic' $CONFIG_PATH)"
PROTOCOL="$(jq --raw-output '.protocol' $CONFIG_PATH)"
FREQUENCY="$(jq --raw-output '.frequency' $CONFIG_PATH)"
GAIN="$(jq --raw-output '.gain' $CONFIG_PATH)"
OFFSET="$(jq --raw-output '.frequency_offset' $CONFIG_PATH)"

# Start the listener and enter an endless loop
echo "Starting RTL_433 with parameters:"
echo "MQTT Host =" $MQTT_HOST
echo "MQTT Port =" $MQTT_PORT
echo "MQTT User =" $MQTT_USER
echo "MQTT Password =" $MQTT_PASS
echo "MQTT Topic =" $MQTT_TOPIC
echo "RTL_433 Protocol =" $PROTOCOL
echo "RTL_433 Frequency =" $FREQUENCY
echo "RTL_433 Gain =" $GAIN
echo "RTL_433 Frequency Offset =" $OFFSET

#set -x  ## uncomment for MQTT logging...

/usr/local/bin/rtl_433 -F json -R $PROTOCOL -f $FREQUENCY -g $GAIN -p $OFFSET | while read line
do
  DEVICE="$(echo $line | jq --raw-output '.model' | tr -s ' ' '_')" # replace ' ' with '_'
  DEVICEID="$(echo $line | jq --raw-output '.id' | tr -s ' ' '_')"

  MQTT_PATH=$MQTT_TOPIC

  if [ ${#DEVICE} > 0 ]; then
    MQTT_PATH=$MQTT_PATH/"$DEVICE"
  fi
  if [ ${#DEVICEID} > 0 ]; then
    MQTT_PATH=$MQTT_PATH/"$DEVICEID"
  fi

  # Create file with touch /tmp/rtl_433.log if logging is needed
  [ -w /tmp/rtl_433.log ] && echo $line >> rtl_433.log
  echo $line | /usr/bin/mosquitto_pub -h $MQTT_HOST -p $MQTT_PORT -u $MQTT_USER -P $MQTT_PASS -i RTL_433 -r -l -t $MQTT_PATH
done
