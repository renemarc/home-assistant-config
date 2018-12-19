<!-- Header -->
[link-profile]:https://github.com/renemarc
[link-repo]:https://github.com/renemarc/home-assistant-config

<a name="top"></a>
<code>[renemarc][link-profile] / **[home-assistant-config][link-repo]** / **cameras** /</code>

<p align="right"><sub><strong><a href="https://github.com/renemarc/home-assistant-config">🏠 Home Assistant configuration for a smart-looking place! 😎</a><br>Be sure to <a href="#" title="star">⭐️</a> this repo!</strong></sub></p>

<!-- Hero -->
<figure>
    <div align="center">
        <a href="#-environment_canadayaml"><img src="../www/screenshots/card-radar-rain.png" alt="Environment Canada rain radar map" title="Environment Canada Rain" width="280"></a>
        <a href="#-environment_canadayaml"><img src="../www/screenshots/card-radar-snow.png" alt="Environment Canada snow radar map" title="Environment Canada Snow" width="280"></a>
    </div>
    <div align="center">
        <a href="#-noaayaml" title="NOAA's GOES-East satellite images"><img src="../www/screenshots/card-satellite-geocolour.jpg" alt="NOAA GeoColour satellite image of North-America's East Coast" title="NOAA GeoColour satellite image" width="280"></a>
        <a href="#-noaayaml" title="NOAA's GOES-East satellite images"><img src="../www/screenshots/card-satellite-vapour.jpg" alt="NOAA Water Vapour satellite image of North-America's East Coast" title="NOAA Water Vapour satellite image" width="280"></a>
    </div>
</figure>

<h1 align="center">Cameras</h1>

Camera sensors are used to fetch and display web images in [`/appdaemon/dashboards/`](../appdaemon/dashboards).

## Weather cameras

### [`📡 ./environment_canada.yaml`](environment_canada.yaml)

[Environment Canada](https://weather.gc.ca/radar/)'s rain and snow radar maps for the last 30 minutes or so, gathered to create simple animations in [`/appdaemon/dashboards/Weather.dash`](../appdaemon/dashboards/Weather.dash).

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-radar-rain.png" alt="Environment Canada rain radar map" title="Environment Canada Rain" width="325">
            <img src="../www/screenshots/card-radar-snow.png" alt="Environment Canada snow radar map" title="Environment Canada Snow" width="325">
        </div>
        <figcaption>
            <p><strong>Environment Canada weather radar maps.</strong></p>
        </figcaption>
    </figure>
</div>

### [`🛰 ./noaa.yaml`](noaa.yaml)

NOAA's (U.S. National Oceanic and Atmospheric Administration) colourized and water vapour [GOES-East satellite images](https://www.star.nesdis.noaa.gov/GOES/GOES16_sectors.php?sector=ne) for the current air masses. Unlike the radar maps above these are not animated in the dashboards because precision is less relevant at those scales.

<div align="center">
    <figure>
        <div>
            <img src="../www/screenshots/card-satellite-geocolour.jpg" alt="NOAA GeoColour satellite image of North-America's East Coast" title="NOAA GeoColour satellite image" width="325">
            <img src="../www/screenshots/card-satellite-vapour.jpg" alt="NOAA Water Vapour satellite image of North-America's East Coast" title="NOAA Water Vapour satellite image" width="325">
        </div>
        <figcaption>
            <p><strong>NOAA GOES-East satellite images for North-America's East Coast.</strong></p>
        </figcaption>
    </figure>
</div>

<p align="right"><a href="#top" title="Back to top">🔝</a></p>

## Other

### [`🖼 ./wallpapers.yaml`](wallpapers.yaml)

Pretty daily pictures from [Bing](https://bing.com) and [NASA](https://apod.nasa.gov/apod/astropix.html), showcased in [`/appdaemon/dashboards/Main.dash`](../appdaemon/dashboards/Main.dash).

<!-- Footer -->
<p align="right"><a href="#top" title="Back to top">🔝</a></p>

<p align="center"><strong>Don't forget to <a href="#" title="star">⭐️</a> this repo! 😃</strong></p>

[🏠 Home][link-repo]
