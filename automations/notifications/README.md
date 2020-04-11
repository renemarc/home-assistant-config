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

### [`🗣️ ./daily_greeting.yaml`](daily_greeting.yaml)

Greet the day with an uplifting text-to-speech daily briefing, like this one:

#### [▶️ Listen to the following daily greeting audio sample](https://instaud.io/2Eye?autoplay=1)

>
> **(( bell ))**
>
> Good morning beautiful people!
>
> We are Saturday September 1st and it is 5 minutes to 9.
>
> Outside temperature is 19˚ but feels like 21.
>
> It will be clear for the hour and will be partly cloudy starting this afternoon, continuing until tomorrow morning.
>
> A light breeze is blowing from the West.
>
> Air quality is good, UV index is moderate and the sun will set at around 7 and a half.
>
> Have a nice day!
>
> You are fabulous!
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## General purpose

### [`🚪 ./door_notify.yaml`](door_notify.yaml)

Warn someone if a door was left open for too long.

Notifications are sent whenever at least one door has been left open for a while, and reminders are then sent every few minutes until all doors are closed. Only a few reminders are sent out however, to avoid notification spam when a door has actually been purposefully left open (for example, while moving things in and out).

#### Door text notification sample

>
> **Home security issue**
>
> A door has been left open for too long.\
> Location: Front door.\
> No further notifications will be sent about this issue until it gets resolved.
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🔄 ./door_notify_reset.yaml`](door_notify_reset.yaml)

Reset door notifications counter.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🚪 ./front_door_notify.yaml`](front_door_notify.yaml)

Warn whenever the front door is opening or closing.

Flashes some lights briefly. Useful to indicate to an otherwise oblivious showering partner that someone likely just came in or left the premises.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⚗️ ./humidity_notify.yaml`](humidity_notify.yaml)

Check if humidity is too high or too low.

Comfort level should be between 35% and 55%. Mold grows above 55% relative humidity, and thrives above 70%. Only verify if doors and windows are closed.

#### [▶️ Listen to the following humidity notification audio sample](https://instaud.io/2Idw?autoplay=1)

>
> **(( alarm ))**
>
> Indoor humidity is way too high.
>
> Currently at 85%.
>
> There is a risk of mold!
> 
> Do reduce the humidity NOW!
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🇨🇺 ./humidor_notify.yaml`](humidor_notify.yaml)

Check if humidity is too high or too low in the humidor.

Cigars should be kept in a humidity-controlled environment, between 65% and 74%, with the ideal sweet spot at 70%.

Notifications are sent whenever humidity levels cross boundaries, and reminders are then sent every few hours until levels get back to normal. Only a few reminders are sent out however, to avoid notification spam when action cannot immediately be taken to bring humidity levels back to normal (say, while out of town).

#### Humidor text notification sample

>
> **Humidor is getting dry**
>
> 60% humidity is too low.\
> Add some distilled water to its humidifier.
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🔄 ./humidor_notify_reset.yaml`](humidor_notify_reset.yaml)

Reset humidor notifications counter.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🌊 ./leak_notify.yaml`](leak_notify.yaml)

Check if a water leak is detected somewhere.

#### [▶️ Listen to the following leak notification audio sample](https://instaud.io/2IdA?autoplay=1)

>
> **(( alarm ))**
>
> A leak has been detected.
>
> Check the kitchen floor.
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⚡ ./power_supply_notify.yaml`](power_supply_notify.yaml)

Check if Raspberry Pi's power supply is providing enough energy.

#### Power supply text notification sample

>
> **Raspbery Pi power issue**
>
> An under-voltage has occurred. (Code 1000)
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`☢️ ./radon_notify.yaml`](radon_notify.yaml)

Check if radon levels are too high.

Radon (Rn) is an element that comes from the natural decay of underground uranium, thorium, and radium. It is a radioactive, colorless, and odorless noble gas. Radon-222 tends to accumulate in enclosed locations like houses. It has a short half-life of 3.8 days before decaying into other short-lived radioactive gases (Polonium-218, Lead-214, Bismuth-214, Polonium-214) then into solid, long-lasting, radiactive Lead-210. This means that when breathing in air or dust particles, radioactive isotopes either transmutate or get deposited inside the lungs, increasing the odds of developping lung cancer. Keeping a place well ventilated is a good way to mitigate this risk.

Notifications are sent whenever radon levels reach tresholds, and reminders are then sent every few hours until levels get back to normal. Only a few reminders are sent out however, to avoid notification spam when action cannot immediately be taken to bring radiation levels back to normal (say, while out of town).

#### References

- [Airthings: Radon levels, what do they mean?](https://airthings.com/us/radon-levels/)
- [WikiPedia: Radon concentration scale](https://en.wikipedia.org/wiki/Radon#Concentration_scale)
- [WHO: Radon and health](https://www.who.int/news-room/fact-sheets/detail/radon-and-health)

#### [▶️ Listen to the following radon notification audio sample](https://instaud.io/2IeI?autoplay=1)

>
> **(( alarm ))**
>
> Radon levels are WAY too high.
>
> Radiation is currently at 215 Bq/m3, which is dangerous.
>
> Air out the place NOW, and start looking into mitigation solutions!
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🔄 ./radon_notify_reset.yaml`](radon_notify_reset.yaml)

Reset radon notifications counter.

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`⚠️ ./smoke_notify.yaml`](smoke_notify.yaml)

Warn someone if the smoke detector has been triggered.

#### Smoke text notification sample

>
> **Smoke alert**
>
> The siren is alerting those inside.\
> Do check with the neighbors!\
> Location: Smoke detector.
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🖐 ./tamper_notify.yaml`](tamper_notify.yaml)

Warn someone if the tamper flag has changed.

#### Tamper text notification sample

>
> **Home security issue**
>
> A perimeter device has been tampered with.\
> Device: Front door.\
> Current state: Tampered.
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

### [`🆕️ ./update_notify.yaml`](update_notify.yaml)

Notify when a new version of Home Assistant is available.

#### Update text notification sample

>
> **Home Assistant update**
>
> Version 1.0 is available.\
> Installed version: 0.83.3
>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Customization

The bulk of the customization is done in [`/customize.yaml`](../../customize.yaml) and [`/customize_glob.yaml`](../../customize_glob.yaml).

The looks of many state cards depend on Custom UI and other templates in [`/www/custom_ui/`](../../www/custom_ui).

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🔙 Back to `/automations/`](../)

[🏠 Home][link-repo]
