# Cameras

I use camera sensors to fetch and display web images in [`/appdaemon/dashboards/`](../appdaemon/dashboards).

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


## Other

### [`🖼 ./wallpapers.yaml`](wallpapers.yaml)

Pretty daily pictures from [Bing](https://bing.com) and [NASA](https://apod.nasa.gov/apod/astropix.html), showcased in [`/appdaemon/dashboards/Main.dash`](../appdaemon/dashboards/Main.dash) 
