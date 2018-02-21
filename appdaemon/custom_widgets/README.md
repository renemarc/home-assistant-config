# Custom AppDaemon widgets

AppDaemon offers [many widgets](https://github.com/home-assistant/appdaemon/tree/dev/appdaemon/widgets/), but can support some third-party and custom ones.


## Community widgets

- [`baseiconsensor`](baseentitydisplay) from [ReneTode's repo]([)https://github.com/ReneTode/My-AppDaemon/tree/master/custom_widgets), modified with:
    + Support for entities used as **title** and **title2**.

- [`baseselect`](baseentitydisplay) also from [ReneTode's repo](https://github.com/ReneTode/My-AppDaemon/tree/master/custom_widgets), modified with:
    + Support for **sub_entities**.


## Custom widgets

- [`baseentitydisplay`](baseentitydisplay) is based on the default [basedisplay](https://github.com/home-assistant/appdaemon/tree/dev/appdaemon/widgets/basedisplay) but with the following modifications:
    + Support for entities used as **title** and **title2**.
    + Include **unit_of_measurement** to the **sub_entity**, if any.

- [`baseentityiframe`](baseentityiframe) is based on the default [baseiframe](https://github.com/home-assistant/appdaemon/tree/dev/appdaemon/widgets/baseiframe) but includes:
    + Cache-buster added to already parameterized URLs.
    + Optional **cache** integer parameter to add longevity to the cache-buster JS parameter.

- [`basemultisensor`](basemultisensor) is like **baseentitydisplay** above, but adds:
    + List two sensors size by side (useful to showcase both _temperature_ and _humidity_ together). 


## Configuration

The extra styling of these widgets is done in the theme [`/appdaemon/custom_css/modern`](../custom_css/modern) as well as directly in [`/appdaemon/dashboards`](../dashboards).
