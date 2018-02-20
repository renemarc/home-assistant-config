function baseentitydisplay(widget_id, url, skin, parameters)
{
    // Will be using "self" throughout for the various flavors of "this"
    // so for consistency ...

    self = this;

    // Initialization

    self.widget_id = widget_id;

    // Store on brightness or fallback to a default

    // Parameters may come in useful later on

    self.parameters = parameters;

    var callbacks = [];

    // Define callbacks for entities - this model allows a widget to monitor multiple entities if needed
    // Initial will be called when the dashboard loads and state has been gathered for the entity
    // Update will be called every time an update occurs for that entity

    self.OnTitleStateAvailable = OnTitleStateAvailable;
    self.OnTitleStateUpdate = OnTitleStateUpdate;
    self.OnTitle2StateAvailable = OnTitle2StateAvailable;
    self.OnTitle2StateUpdate = OnTitle2StateUpdate;
    self.OnStateAvailable = OnStateAvailable;
    self.OnStateUpdate = OnStateUpdate;
    self.OnSubStateAvailable = OnSubStateAvailable;
    self.OnSubStateUpdate = OnSubStateUpdate;

    var monitored_entities =  [];

    if ("title_entity" in parameters && parameters.title_entity != "")
    {
        monitored_entities.push({"entity": parameters.title_entity, "initial": self.OnTitleStateAvailable, "update": self.OnTitleStateUpdate});
    }
    if ("title2_entity" in parameters && parameters.title2_entity != "")
    {
        monitored_entities.push({"entity": parameters.title2_entity, "initial": self.OnTitle2StateAvailable, "update": self.OnTitle2StateUpdate});
    }
    if ("entity" in parameters)
    {
        monitored_entities.push({"entity": parameters.entity, "initial": self.OnStateAvailable, "update": self.OnStateUpdate});
    }
    if ("sub_entity" in parameters && parameters.sub_entity != "")
    {
        monitored_entities.push({"entity": parameters.sub_entity, "initial": self.OnSubStateAvailable, "update": self.OnSubStateUpdate});
    }

    // Finally, call the parent constructor to get things moving

    WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks);

    // Function Definitions

    // The StateAvailable function will be called when
    // self.state[<entity>] has valid information for the requested entity
    // state is the initial state
    // Methods

    function OnTitleStateAvailable(self, state)
    {
        set_title_value(self, state);
    }

    function OnTitleStateUpdate(self, state)
    {
        set_title_value(self, state);
    }

    function OnTitle2StateAvailable(self, state)
    {
        set_title2_value(self, state);
    }

    function OnTitle2StateUpdate(self, state)
    {
        set_title2_value(self, state);
    }

    function OnStateAvailable(self, state)
    {
        set_value(self, state);
    }

    function OnStateUpdate(self, state)
    {
        set_value(self, state);
    }

    function OnSubStateAvailable(self, state)
    {
        set_sub_value(self, state);
    }

    function OnSubStateUpdate(self, state)
    {
        set_sub_value(self, state);
    }

    function set_title_value(self, state)
    {
        self.set_field(self, "title", state.state);
    }

    function set_title2_value(self, state)
    {
        self.set_field(self, "title2", state.state);
    }

    function set_value(self, state)
    {
        value = self.map_state(self, state.state);
        if (isNaN(value))
        {
            self.set_field(self, "value_style", self.parameters.css.text_style);
            self.set_field(self, "value", self.map_state(self, value));
        }
        else
        {
            self.set_field(self, "value_style", self.parameters.css.value_style);
            self.set_field(self, "value", self.format_number(self, value));
            self.set_field(self, "unit_style", self.parameters.css.unit_style);
            if ("units" in self.parameters)
            {
                self.set_field(self, "unit", self.parameters.units);
            }
            else
            {
                self.set_field(self, "unit", state.attributes["unit_of_measurement"]);
            }
        }
    }

    function set_sub_value(self, state)
    {
        if ("sub_entity_map" in self.parameters)
        {
            self.set_field(self, "state_text", self.parameters.sub_entity_map[state.state]);
        }
        else
        {
            value = self.map_state(self, state.state);
            if (isNaN(value))
            {
                self.set_field(self, "state_text", state.state);
            }
            else
            {
                self.set_field(self, 'state_text',
                    self.format_number(self, value) +
                    (state.attributes.unit_of_measurement ?
                        ' ' + state.attributes.unit_of_measurement :
                        ''
                    )
                );
            }
        }
    }

}
