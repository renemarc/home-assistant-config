# Home Assistant config.

Configuration for Home Assistant running Hass.io on a Raspberry Pi for a one bedroom appartment.

Goals:
- Devices and sensors must be modular and easy to replace without much recoding.
- Instantly usable by anyone.
- Not everything should be networked: pantry and laundry room lights have their independent motion sensors and that's a good thing.

Logic:
- I like tech alright, but like good butlers it should stay out of sight but summonable when desired.
- As much local processing as possible.
- Accessible through multiple ways: computer, tablet kiosk, voice, smart phones, FLIC switches.
- Easy to read information: no information overload, not too much granularity yet not too vague, just right.
- Intuitive user interface: One look as a group of sensors/switches should be sufficient for anyone to understand the currrent conditions.
- Simple, intuitive navigation.


- No indoor cameras: I don't need to invite Big Brother in.
- No Google Voice: idem, I don't need to have the world's largest advertising agency listening in to everything I say just for the convenience of it turning on my lights using my voice.

## Devices
- Lifx+ light bulbs (x2)
- Lifx Z light strips (x5)
- Nanoleaf Aurora
- Frigidaire dehumidifier.
- Sunbeam humidifier.
- Sharp plasmacluster air purifier.
- Oscillating fan.
- TP-Link mini wifi outlets (x6)
- Aeotec minimote
- Aeotec Z-stick
- Aeotec multisensor 6
- Aeotec door/window sensor
- Adalight/Ambilight (Prismatik) 100-dots TV backlighting on HTPC.

## Features implemented
### Climate control
- Low/High humidity alerts
- Mold conditions alert
- Temperature monitor (pantry, bedroom, living room)
- Humidity monitor (living room, bedroom)
- Turn Dehumidifier on in afternoon when humidity too high
- Turn dehumidifier/air purifier off when windows open or when front door opened for more than 5 minutes.


### Weather report
- Weather report
- Weather: Dark Sky data using easy-to-read status and forecast.
- Outdoor pollution report
- Weather radar maps

### Lighting control
- Control all pluggable lights
- Ambilight/Prismatik TV bias lighting control (start, stop, status)
- Nanoleaf Aurora control (start, stop, status, change scene)
- Flux-like white temperature shift based on active hours, not daylight. (with up-to-the-second precision)
- Automation: Change Aurora lights based on day/scene
- Manual theme for Aurora
- Manual theme for Lifx Z
- Change LIFX Z colours based on day/scene
- Full-schedule for Lifx Z

### Automations
- Pulse shower light when front door opens/closes.
- Automation: Auto CCT based on time of day + sleep pattern

### Scenes
- Good night, good morning, nap time
- Movie scene (dim lights)

### Human Interface Devices
- FLIC switches (bedroom)
- Homebridge
- Tablet dashboard for wall-mounted interface
- Cellphone command (app)
- Dashboard: switchboard


### Physical sensors
- Window sensor (living room, front door)
- Door sensor (front, internal back)

### Other
- HA status monitoring: Average Load, RAM use, Disk use
- Network status monitoring: Uptime, Download
- Next bus schedules
- Doomsday clock
- Optimize bus schedule database query (semi-fail)


### TO FIX:
- Dashboard: main panel
- Dashboard: status panel
- Dashboard: custom sensors refresh rate
- ISP: fix eBox unlimited bug
- Status: Update available (URL fetch)
- State card for text only (weather, quotes...)

### TO FIX (eventual)
- ISP: use USB gigabit connection (required new device)
- Movement nightlight (requires new device)

### TODO:
- Overrides for each automation
- Full-schedule for Aurora
- Voice command
- Away mode
- Romantic scene
- Synthwave/Gaming Scene
- Presence detection (iPhone)

### IDEAS (high priority)
- Dashboard: context-aware link widgets
- LIFZ strips under bed
- kitchen under-cabinet lighting
- FLIC switch (kitchen)

### IDEAS (medium priority)
- Welcome home front door trigger
- Door/Window sensor temper alert
- daily picture

### IDEAS (low priority)
- Indoor climate/pollution sensing and report
- Exterior light
- APCUPSD
- Monitor humidity in humidor
- PIHole Status
- Light patterns in windowed cabinets
- Motion nightlight in bathroom above sink
- Fade in/out fairy lights and bedside lamp
- Read rooftop weather station (Fine Offset WH1080)
- Timer-based, fade in/out, twinkling Christmas tree
