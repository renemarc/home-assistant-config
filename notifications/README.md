<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **notifications** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>


<!-- Hero -->
<figure>
    <div align="center">
        <a href="#notifications" title="Notifications"><img src="https://media.giphy.com/media/1TxPkOmF3y2Lm/giphy.gif" alt="Ralh from The Simpsons playing with a mailbox"></a>
    </div>
</figure>


<h1 align="center">Notifications</h1>

Useful during development of automations, I later keep using them for simple warnings like when the dehumidifier is likely full in [`/automations/humidity_notify.yaml`](../automations/humidity_notify.yaml)  or if a door has been left open for too long in [`/automations/doors_notify.yaml`](../automations/doors_notify.yaml).


## Files

### [`👪 ./group.yaml`](group.yaml)

Notifications services are organized into higher-level [notification groups](https://home-assistant.io/components/notify.group/), to avoid peppering hard-coded services throughout automations.


### [`📢 ./lannouncer.yaml`](lannouncer.yaml)

For audio alerts and text-to-speech messages sent to the [LANnouncer](http://www.keybounce.com/lannouncer/) Android app running on the kiosk. To make sure that LANnouncer is available after a reboot, the app gets launched using [AutoStart - No root](https://play.google.com/store/apps/details?id=com.autostart).


### [`💬 ./pushover.yaml`](pushover.yaml)

Notification service for cellphones and tablets. I was already using [Pushover](https://pushover.net) for other purposes, so might as well continue.


### [`🔗 ./rest.yaml`](rest.yaml)

For text-to-speech messages sent to the [Fully Kiosk Browser](http://www.keybounce.com/lannouncer/). Currently placed in stand-by in case LANnouncer becomes unresponsive again.


<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
