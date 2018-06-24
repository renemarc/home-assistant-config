# Custom UI state cards

These state cards are used to adapt the looks of Home Assistant sensors for easier information consumption.

## Third-party state cards

### [`🌈 ./scripts(-es5?).js(.map|LICENSE)`](scripts.js.map)

Debuging and development files for **Custom UI elements** below.


### [`🌈 ./state-card-custom-ui(-es5?).html(.gz?)`](state-card-custom-ui.html)

[Custom UI elements](https://github.com/andrey-git/home-assistant-custom-ui) help improve the display of sensors and jazz up the interface a bit.

<div align="center">
    <figure>
        <div>
            <img src="../screenshots/group-weather.png" alt="Weather group" title="Custom UI elements + Value-only state card" width="325">
            <img src="../screenshots/group-climate.png" alt="Climate Control group" title="Custom UI elements + custom card theme" width="325">
        </div>
        <figcaption>
           <p><strong>Custom UI elements.</strong></p>
        </figcaption>
    </figure>
</div>


### [`➖ ./state-card-hline(_es5?).html`](state-card-hline.html)

[Horizontal line state card](https://github.com/covrig/homeassistant-hline) to visually separate long lists of sensors.

<div align="center">
    <figure>
        <div>
            <img src="../screenshots/card-horizontal-line.png" alt="Horizontal line state card" title="Custom UI + Horizontal line state card" width="325">
        </div>
        <figcaption>
            <p><strong>Horizontal line state card.</strong></p>
        </figcaption>
    </figure>
</div>


### [`📝 ./state-card-value_only.html`](state-card-value_only.html)

[Value-only state card](https://community.home-assistant.io/t/display-only-text-in-card/20536/26) for wordy sensor states.

<div align="center">
    <figure>
        <div>
            <img src="../screenshots/group-forecast.png" alt="Value-only state card" title="Value-only state card" width="325">
        </div>
        <figcaption>
            <p><strong>Value-only state card.</strong></p>
        </figcaption>
    </figure>
</div>


## Customization

Actual customization of state cards is done in [`/customize.yaml`](../../customize.yaml) and [`/customize_glob.yaml`](../../customize_glob.yaml).
