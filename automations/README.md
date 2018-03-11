# Automations

## Publishers and subscribers

To prevent _spaghettification_ of automations as this project grows, I employ a [publish–subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) (kind of a lightweight [mediator pattern](https://en.wikipedia.org/wiki/Mediator_pattern)) where some automations will trigger changes on [`/misc/input_booleans.yaml`](../misc/input_booleans.yaml) and [`/misc/variables.yaml`](../misc/variables.yaml) while others listen to those changes.

For example, one push of a button will lead to enabling the **night mode** by setting the relevant boolean to _true_. Every room has an automation that listens to changes on that **night mode** boolean, and is responsible for turning devices on and off accordingly. This makes every room reactive to one central direction, without having to maintain a monolithic [`/scripts/go_to_sleep.yaml`](../scripts/go_to_sleep.yaml) that lists all the devices that must be acted upon.

It's a bit like a boss giving orders to managers, and letting them figure out how to best accomplish these goals based on what they know about their respective teams. Less micromanagement = smarter teams.

In the comments, automations annotated with **@publish** are the ones that issue orders, and those annotated with **@subscribe** are listening for such orders. Some automations will be both **publishers** and **subscribers** of different orders.
