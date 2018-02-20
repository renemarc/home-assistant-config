# AppDaemon 2.0 dashboards

These are dashboards to be used in a wall-mounted tablet to control Home Assistant the same way you would on a computer, only in a more appropriate interface for casual and often-on display.

Most implementations of AppDaemon/HADashboard focus on having a car-like in-dash interface and overloading the screen with tons of sensors. That leads to a poor user experience in my opinion.

When using a large-enough format tablet, I prefer intuitive interfaces like the ones you are familiar with on fixed-width websites. Intuitive navigation, just enough data to feel at ease without being overwhelmed. And it must be pretty-enough to be hung on a wall ...literally!

These dashboards target a 10" display tablet with 1024x800 resolution using a full-screen browser. In my case I use Adroid and the [Fully Kiosk Browser](http://www.ozerov.de/fully-kiosk-browser/) with the status-bar active on a white [Acer Iconia One](https://www.acer.com/ac/en/CA/content/series/iconiaone10). It's great for this usage: it has an IPS display, is relatively inexpensive, looks good, has a responsive touchscreen, is snappy enough with its 2GB of RAM, is made to be held at the horizontal, and has a top-mounted front-camera for eventual screen wake-up on motion. I have it held in place using [Koala damage-free wall-mounts](https://www.dockem.com/category-s/1861.htm) in a central location, and it is permanently hooked to USB power.


## Organization

Dashboards are split into 4 pages, organized in a similar fashion as [`/groups`](../../groups) only with less administrative features and prettier colours.


### Fixed elements

The top menu and left-hand navigation are fixed. The navigation colours change depending on which dashboard you're on and the top menu title changes accordingly. That makes navigation intuitive for anyone.


### Main dashboard

With a feel-good welcome message, common actions, quick weather status, bus schedules, and rotating set of weather radar, satellite maps and pretty pictures of the day.


### Switchboard

Organized my room and control zone, including climate control. Looks kind of like Tetris! :-)


### Weather

With current conditions, forecasts, air quality, and rotating satellite maps and animated radar maps.


### Status

Geeky details about Home Assistant, network, battery status and per-location temperature and humidity.


## Theme

The [`/appdeamon/custom_css/modern`](../custom_css/modern) theme is based on an adapted version of the default theme. Only some CSS rules differ, in addition to support for third-party and custom widgets.

The contents of many tiles depend on specific [template sensors](../../sensors) to make information easier to digest.
