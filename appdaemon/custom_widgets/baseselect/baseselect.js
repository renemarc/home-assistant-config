function baseselect(widget_id, url, skin, parameters)
{
    // Will be using "self" throughout for the various flavors of "this"
    // so for consistency ...

    self = this;

    // Initialization

    self.widget_id = widget_id;

    // Store on brightness or fallback to a default

    // Parameters may come in useful later on

    self.parameters = parameters;

    self.onChange = onChange;

    var callbacks = [
            {"selector": '#' + widget_id + ' > div > select', "action": "change", "callback": self.onChange},
                    ];


    // Define callbacks for entities - this model allows a widget to monitor multiple entities if needed
    // Initial will be called when the dashboard loads and state has been gathered for the entity
    // Update will be called every time an update occurs for that entity

    self.OnStateAvailable = OnStateAvailable;
    self.OnStateUpdate = OnStateUpdate;
    self.OnSubStateAvailable = OnSubStateAvailable;
    self.OnSubStateUpdate = OnSubStateUpdate;

    var monitored_entities = [];

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

    function OnStateAvailable(self, state)
    {
        self.state = state.state;
        set_options(self, state.attributes.options, state);
        set_value(self, state);
    }

    function OnSubStateAvailable(self, state)
    {
        set_sub_value(self, state);
    }

    function OnStateUpdate(self, state)
    {
        self.state = state.state;
        set_value(self, state);
    }

    function OnSubStateUpdate(self, state)
    {
        set_sub_value(self, state);
    }

    function set_value(self, state)
    {
        value = self.map_state(self, state.state);
        self.set_field(self, "selectedoption", value);
        if ("state_text" in self.parameters && self.parameters.state_text == 1)
        {
            self.set_field(self, "state_text", self.map_state(self, state));
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
            self.set_field(self, "state_text", state.state);
        }
    }

    function onChange(self, state)
    {
        setTimeout(function(){
            if (self.state != self.ViewModel.selectedoption())
            {
                self.state = self.ViewModel.selectedoption();
                args = self.parameters.post_service;
                args["option"] = self.state;
                self.call_service(self, args);
            }
        },500);
    }

    function set_options(self, options, state)
    {
        self.set_field(self, "inputoptions", options);
    }

}
