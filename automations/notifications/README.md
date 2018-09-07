<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / [automations](..) / **notifications** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>


<!-- Hero -->
<figure>
    <div align="center">
        <a href="#notifications-automations" title="Notifications automations"><img src="https://media.giphy.com/media/l2JJBaRkb0olgJfUY/giphy.gif" alt="You are still alone phone notification"></a>
    </div>
</figure>


<h1 align="center">Notifications automations</h1>

Visual and audio notifications are regrouped here for clarity. Mobile text alerts are kept to a minimum to limit non-critical, annoying disturbances.


## Greetings

### [`🗣️️ ./daily_greeting.yaml`](daily_greeting.yaml)

Greet the day with an uplifting text-to-speech daily briefing, like this one:

> [▶️ Listen](https://instaud.io/2Eye)
> 
> > Good morning beautiful people!
> > 
> > We are Saturday September 1st and it is 5 minutes to 9.
> > 
> > Outside temperature is 19˚ but feels like 21.
> > 
> > It will be clear for the hour and will be partly cloudy starting this afternoon, continuing until tomorrow morning.
> > 
> > A light breeze is blowing from the West.
> > 
> > Air quality is good, UV index is moderate and the sun will set at around 7 and a half.
> > 
> > Have a nice day!
> > 
> > You are fabulous!
> 
> <sub><strong>Audio sample recorded using [ttsMP3]( https://ttsmp3.com/) and hosted by [Instaudio](https://instaud.io/).</strong></sub>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


## General purpose

### [`🚪 ./doors_notify.yaml`](doors_notify.yaml)

Warn someone if a door was left open for too long.


### [`🚪️ ./front_door_notify.yaml`](front_door_notify.yaml)

Warn whenever the front door is opening or closing.


### [`⚗️️ ./humidity_notify.yaml`](humidity_notify.yaml)

Check if humidity is too high or too low.


### [`🇨🇺 ./humidor_notify.yaml`](humidor_notify.yaml)

Check if humidity is too high or too low in the humidor.


### [`🌊 ./leak_notify.yaml`](leak_notify.yaml)

Check if a water leak is detected somewhere.


### [`⚡ ./power_supply_notify.yaml`](power_supply_notify.yaml)

Check if Raspberry Pi's power supply is providing enough energy.


### [`🖐 ./tamper_notify.yaml`](tamper_notify.yaml)

Warn someone if the tamper flag has changed.


### [`🆕️ ./update_notify.yaml`](update_notify.yaml)

Notify when a new version of Home Assistant is available.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>


## Customization

The bulk of the customization is done in [`/customize.yaml`](../../customize.yaml) and [`/customize_glob.yaml`](../../customize_glob.yaml).

The looks of many state cards depend on Custom UI and other templates in [`/www/custom_ui/`](../../www/custom_ui).


<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🔙 Back to `/automations/`](../)

[🏠 Home][link-repo]
