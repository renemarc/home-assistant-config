function baseentityiframe(widget_id, url, skin, parameters)
{
    self = this;

    // Initialization

    self.parameters = parameters;

    var callbacks = [];

    var monitored_entities = [];

    var _titles = [];

    // Define dynamic methods.
    if ("title_entity_list" in self.parameters)
    {
        function record_title_value(self, state, idx)
        {
            _titles[idx] = state.state;
        }
        self.record_title_value = record_title_value;

        self.title_index = 0;

        // Set title entities changes to be recorded.
        var nameAvailable, nameUpdate, funcAvailable, funcUpdate,
        title_size = self.parameters.title_entity_list.length;

        for (var i = 0; i < title_size; ++i)
        {
            _titles[i] = '';
            entity_title = self.parameters.title_entity_list[i];
            if (entity_title.trim() != "") {
                nameAvailable = "OnTitle" + self.title_index + "StateAvailable";
                funcAvailable = new Function(
                     "return function " + nameAvailable + "(self, state){ self.record_title_value(self, state, " + self.title_index + ");}"
                )();
                Object.defineProperty(self, nameAvailable, {value: funcAvailable, writable: false});

                nameUpdate = "OnTitle" + self.title_index + "StateUpdate";
                funcUpdate = new Function(
                     "return function " + nameUpdate + "(self, state){ self.record_title_value(self, state, " + self.title_index + ");}"
                )();
                Object.defineProperty(self, nameUpdate, {value: funcUpdate, writable: false});

                monitored_entities.push({"entity": entity_title, "initial": self[nameAvailable], "update": self[nameUpdate]});
            }
            self.title_index = self.title_index + 1;
        }
    }

    // Call the parent constructor to get things moving

    WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks)

    // Set the url

    if ("url_list" in parameters || "img_list" in parameters || "entity_picture" in parameters)
    {
        self.index = 0;
        refresh_frame(self)
    }

    self.cache = 0;
    if ("cache" in parameters)
    {
        self.cache = parameters.cache;
    }

    function refresh_frame(self)
    {
        if ("url_list" in self.parameters)
        {
            self.set_field(self, "frame_src", self.parameters.url_list[self.index]);
            self.set_field(self, "img_src", "/images/Blank.gif");
            self.set_field(self, "title", _titles[self.index]);
            size = self.parameters.url_list.length
        }
        else if ("img_list" in self.parameters)
        {
            var url = self.parameters.img_list[self.index];
            var separator = url.indexOf('?') > -1 ? '&' : '?';
            var date = (new Date).getTime();
            var timestamp = Math.floor(date/1000) - (self.cache ? Math.floor(date/1000) % self.cache : 0);
            url = url + separator + "time=" + timestamp;
            self.set_field(self, "img_src", url);
            self.set_field(self, "title", _titles[self.index]);
            size = self.parameters.img_list.length
        }
        else if ("entity_picture" in self.parameters)
        {
            var url = self.parameters.entity_picture;
            var separator = url.indexOf('?') > -1 ? '&' : '?';
            var date = (new Date).getTime();
            var timestamp = Math.floor(date/1000) - (self.cache ? Math.floor(date/1000) % self.cache : 0);
            url = url + separator + "time=" + timestamp;
            self.set_field(self, "img_src", url);
            size = 1
        }

        if ("refresh" in self.parameters)
        {
            self.index = self.index + 1;
            if (self.index == size)
            {
                self.index = 0;
            }
            setTimeout(function() {refresh_frame(self)}, self.parameters.refresh * 1000);
        }
    }
}
