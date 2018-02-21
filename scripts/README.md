# Scripts

For the most part, actions and requirements are based on publish–subscribe pattern where devices and rooms are smart-enough to respond themselves to global parameters and responsible for their own states. See [`/automations`](../automations) and [`/misc/input_booleans.yaml`](../misc/input_booleans.yaml) for details.


## Smart scenes

Smart scenes are a hybrid approach, where global parameters are used when appropriate, and some direct control is employed to achieve a specific setup. They are used both in [`/automations`](../automations) and as a manual selector in [`/misc/input_selects.yaml`](../misc/input_selects.yaml) and [`/appdaemon/dashboards/Main.dash`](../appdaemon/dashboards/Main.dash).


### [`scene_daylight.yaml`](scene_daylight.yaml)

:high_brightness:  Turn on all lights, and set most of the smart ones to a bright daylight white temperature.


### [`scene_default.yaml`](scene_default.yaml)

:house: Used to disable scene mode and return light selectors to their default states.


### [`scene_gaming.yaml`](scene_gaming.yaml)

:space_invader: Set lounge smart lights to video gaming themed colours and effects, as the HTPC is used for gaming also.


### [`scene_movie.yaml`](scene_movie.yaml)

:tv: Enable lounge ambiant lights and set its smart ones to television-friendly colours and effects.

<p align="center">
    <a href="https://youtu.be/sOnqjkJTMaA?t=3m50s" title="Thriller"><img src="https://media.giphy.com/media/pUeXcg80cO8I8/giphy.gif" alt="Michael Jackson in Thriller"></a>
</p>


### [`scene_romantic.yaml`](scene_romantic.yaml)

:heart_eyes: Turn on accent lights, dim some others, pick a romantic colour theme, set the mood for _looooove!_

<p align="center">
    <a href="https://youtu.be/zmTj1oqCBKo?t=14s" title="Giggity!"><img src="https://i.ytimg.com/vi/zmTj1oqCBKo/mqdefault.jpg" alt="Quagmire home automation"></a>
</p>


## Other scripts

### [`wakeup.yaml`](wakeup.yaml)

:sunny: Quickly disable all blocking modes, therefore activating all lights.
