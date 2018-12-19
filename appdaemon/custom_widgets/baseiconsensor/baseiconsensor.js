function baseiconsensor(widget_id, url, skin, parameters)
{
    // Will be using "self" throughout for the various flavors of "this"
    // so for consistency ...

    self = this;

    // Initialization

    self.widget_id = widget_id;

    // Store on brightness or fallback to a default

    // Parameters may come in useful later on

    self.parameters = parameters;
    self.state_icons = self.parameters.state_icons;


    // Define callbacks for on click events
    // They are defined as functions below and can be any name as long as the
    // 'self'variables match the callbacks array below
    // We need to add them into the object for later reference


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

    var monitored_entities = [];

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

    function OnTitleStateAvailable(self, state)
    {
        set_title_value(self, state);
    }

    function OnTitle2StateAvailable(self, state)
    {
        set_title2_value(self, state);
    }

    function OnStateAvailable(self, state)
    {
        self.state = state.state;
        set_view(self, self.state);
    }

    function OnSubStateAvailable(self, state)
    {
        set_sub_value(self, state);
    }

    // The OnStateUpdate function will be called when the specific entity
    // receives a state update - it's new values will be available
    // in self.state[<entity>] and returned in the state parameter

    function OnTitleStateUpdate(self, state)
    {
        set_title_value(self, state);
    }

    function OnTitle2StateUpdate(self, state)
    {
        set_title2_value(self, state);
    }

    function OnStateUpdate(self, state)
    {
        self.state = state.state;
        set_view(self, self.state);
    }

    function OnSubStateUpdate(self, state)
    {
        set_sub_value(self, state);
    }

    // Set view is a helper function to set all aspects of the widget to its
    // current state - it is called by widget code when an update occurs
    // or some other event that requires a an update of the view

    function set_view(self, state)
    {
        if ("icons" in self.parameters)
        {
            if (state in self.parameters.icons)
            {
                self.set_icon(self, "icon", self.parameters.icons[state].icon);
                self.set_field(self, "icon_style", self.parameters.icons[state].style)
            }
            else if ("default" in self.parameters.icons)
            {
                self.set_icon(self, "icon", self.parameters.icons.default.icon);
                self.set_field(self, "icon_style", self.parameters.icons.default.style)
            }
            else
            {
                self.set_icon(self, "icon", "fa-circle-thin");
                self.set_field(self, "icon_style", "color: white")
            }

        }

        if ("state_text" in self.parameters && self.parameters.state_text == 1)
        {
            self.set_field(self, "state_text", self.map_state(self, state))
        }
    }

    function set_title_value(self, state)
    {
        self.set_field(self, "title", state.state);
    }

    function set_title2_value(self, state)
    {
        self.set_field(self, "title2", state.state);
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
}
