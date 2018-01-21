function baseentityiframe(widget_id, url, skin, parameters)
{
    self = this

    // Initialization

    self.parameters = parameters;

    var callbacks = []

    var monitored_entities = []

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
