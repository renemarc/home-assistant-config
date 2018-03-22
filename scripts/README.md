# Scripts

For the most part, actions and requirements are based on publish–subscribe pattern where devices and rooms are smart-enough to respond themselves to global parameters and responsible for their own states. See [`/automations/`](../automations) and [`/misc/input_booleans.yaml`](../misc/input_booleans.yaml) for details.


## Smart scenes

Smart scenes are a hybrid approach, where global parameters are used when appropriate, and some direct control is employed to achieve a specific setup. They are used both in [`/automations/`](../automations) and as a manual selector in [`/misc/input_selects.yaml`](../misc/input_selects.yaml) and [`/appdaemon/dashboards/Main.dash`](../appdaemon/dashboards/Main.dash).


### [`🔆 ./scene_daylight.yaml`](scene_daylight.yaml)

Turn on all lights, and set most of the smart ones to a bright daylight white temperature.

<div align="center">
    <figure>
        <div>
            <a href="https://cheezburger.com/7425309184"><img src="https://media.giphy.com/media/CPutABwbvXC92/giphy.gif" alt="Opening curtains"></a>
        </div>
        <figcaption>
            <p><strong>Daylight!</strong></p>
        </figcaption>
    </figure>
</div>

### [`🏠 ./scene_default.yaml`](scene_default.yaml)

Used to disable scene mode and return light selectors to their default states.


### [`👾 ./scene_gaming.yaml`](scene_gaming.yaml)

Set lounge smart lights to video gaming themed colours and effects, as the HTPC is used for gaming also.

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=x-Wg4mr75yYs" title="Randy March playing video games"><img src="https://media.giphy.com/media/3o6Zt3XykpTtUq39zq/giphy.gif" alt="Randy March playing video games"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=x-Wg4mr75yY" title="Just 5 more minutes...!">Randy March playing video games.</a></strong></p>
        </figcaption>
    </figure>
</div>

### [`📺 ./scene_movie.yaml`](scene_movie.yaml)

Enable lounge ambiant lights and set its smart ones to television-friendly colours and effects.

<div align="center">
    <figure>
        <div>
            <a href="https://youtu.be/sOnqjkJTMaA?t=3m50s" title="Michael Jackson's Thriller music video"><img src="https://media.giphy.com/media/pUeXcg80cO8I8/giphy.gif" alt="Michael Jackson in Thriller"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=sOnqjkJTMaA&t=3m50s" title="Michael Jackson's Thriller music video">♫♬♪ You know it's thriller, Thriller night... ♪♫♬</a></strong></p>
        </figcaption>
    </figure>
</div>

### [`💏 ./scene_romantic.yaml`](scene_romantic.yaml)

Turn on accent lights, dim some others, pick a romantic colour theme, set the mood for _looooove!_

<div align="center">
    <figure>
        <div>
            <a href="https://youtu.be/zmTj1oqCBKo?t=14s" title="Quagmire's home automation. Giggity Giggity!"><img src="https://i.ytimg.com/vi/zmTj1oqCBKo/mqdefault.jpg" alt="Quagmire's home automation"></a>
        </div>
        <figcaption>
           <p><strong><a href="https://youtu.be/zmTj1oqCBKo?t=14s" title="Giggity!">Quagmire's Home Automation.</a> Giggity Giggity!</strong></p>
        </figcaption>
    </figure>
</div>

## Other scripts

### [`👮 ./tamper_reset.yaml`](tamper_reset.yaml)

Reset the state for tampered perimeter devices list.

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=JGAV8wvYdVI" title="The Romantics' One in a Million music video"><img src="https://media.giphy.com/media/sChf4Eo55W8x2/giphy.gif" alt="Reset button"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=JGAV8wvYdVI" title="The Romantics' One in a Million music video">♫♬♪ One in a Million... ♪♫♬</a></strong></p>
        </figcaption>
    </figure>
</div>


### [`☀ ./wake_up.yaml`](wake_up.yaml)

Quickly disable all blocking modes, therefore activating all lights.

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=5_RUut1px3Q" title="Chuck Norris facts"><img src="https://memegenerator.net/img/instances/18858590/i-dont-turn-on-the-light-i-turn-off-the-dark.jpg" alt="Chuck Norris doesn't turn on the light. He turns off the dark." width="400"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=5_RUut1px3Q" title="Chuck Norris facts">Chuck Norris this.</a></strong></p>
        </figcaption>
    </figure>
</div>
