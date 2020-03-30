/*jslint
    browser: true,
    single: true,
    this: true
*/
/*global
    WidgetBase
*/
function baseslideshow(widget_id, url, skin, parameters) {

    // Initialize widget.
    var self = this;
    var callbacks = [];
    var monitored_entities = [];
    var _slides = [];

    var funcAvailable;
    var funcUpdate;
    var item;

    // Define defaults.
    self.parameters = parameters;
    self.base_url = '';
    if (parameters.hasOwnProperty('base_url')) {
        self.base_url = parameters.base_url;
    }
    if (self.base_url === '') {
        self.base_url = window.location.protocol + '//' +
        window.location.hostname + ':8123';
    }

    self.cache = 600;
    if (parameters.hasOwnProperty('cache') && parameters.cache !== '') {
        self.cache = parseInt(parameters.cache);
    }

    self.delay = 10;
    if (parameters.hasOwnProperty('delay') && parameters.delay !== '') {
        self.delay = parseFloat(parameters.delay);
    }

    // Convert each entry into a valid slide.
    self.parameters.slides.forEach(function (entry, i) {
        // Try to determine the type for simple config.
        if (typeof entry === 'string') {
            if (entry.indexOf('/') >= 0) {
                if (entry.match(/\.(gif|jpg|jpeg|png|svg)$/)) {
                    entry = {
                        image: entry
                    };
                } else {
                    entry = {
                        url: entry
                    };
                }
            } else {
                entry = {
                    entity: entry
                };
            }
        }

        // Assemble slide metadata.
        item = {
            type: undefined,
            entity: undefined,
            entity_loaded: false,
            cache: undefined,
            delay: 0,
            stream: false,
            src: undefined,
            name: undefined,
            title: undefined
            // token: undefined
        };
        if (entry.hasOwnProperty('entity') && entry.entity !== '') {
            item.type = 'entity';
            item.entity = entry.entity;
        } else if (entry.hasOwnProperty('image') && entry.image !== '') {
            item.type = 'image';
            item.src = entry.image;
        } else if (entry.hasOwnProperty('url') && entry.url !== '') {
            item.type = 'url';
            item.src = entry.url;
        }
        if (entry.hasOwnProperty('cache') && entry.cache !== '') {
            item.cache = parseInt(entry.cache);
        }
        if (entry.hasOwnProperty('delay') && entry.delay !== '') {
            item.delay = parseFloat(entry.delay);
        }
        if (entry.hasOwnProperty('stream') && entry.stream === 'on') {
            item.stream = true;
        }
        if (entry.hasOwnProperty('title')) {
            item.title = entry.title;
        }
        _slides[i] = item;

        // Monitor image entities.
        if (entry.hasOwnProperty('entity')) {
            funcAvailable = function(self, state, $i) {
                _slides[i].entity_loaded = true;
                _slides[i].src = state.attributes.entity_picture;
                _slides[i].name = state.attributes.friendly_name;
            };
            funcUpdate = function(self, state, $i) {
                _slides[i].src = state.attributes.entity_picture;
                _slides[i].name = state.attributes.friendly_name;
            };

            monitored_entities.push({
                'entity': entry.entity,
                'initial': funcAvailable,
                'update': funcUpdate
            });
        }

        // Monitor optional descriptions.
        if (entry.hasOwnProperty('entity_title')) {
            funcUpdate = function(self, state, $i) {
                _slides[i].title = state.state;
            };

            monitored_entities.push({
                'entity': entry.entity_title,
                'initial': funcUpdate,
                'update': funcUpdate
            });
        }
    });

    WidgetBase.call(
        self,
        widget_id,
        url,
        skin,
        parameters,
        monitored_entities,
        callbacks
    );

    self.index = 0;
    function refresh_frame(self) {
        var cache;
        var date;
        var delay;
        var separator = '?';
        var slide;
        var src;
        var timestamp;
        var title;

        slide = _slides[self.index];

        // Restart frame if entity is not dinamycally loaded yet.
        if (slide.type === 'entity' && slide.entity_loaded === false) {
            self.set_field(self, 'frame_src', '');
            self.set_field(self, 'img_internal_style', 'display: none;');
            self.set_field(self, 'img_src', '/images/Blank.gif');
            self.set_field(self, 'title', '');

            clearTimeout(self.timeout);
            self.timeout = setTimeout(
                function() {
                    refresh_frame(self);
                },
                100
            );
            return;
        }

        // Determine media source.
        switch (slide.type) {
        case 'entity':
            // Set camera API endpoint.
            if (slide.stream) {
                slide.src.replace(
                    '/api/camera_proxy/',
                    '/api/camera_proxy_stream/'
                );
            }
            src = self.base_url + slide.src;
            break;

        case 'image':
        case 'url':
            src = slide.src;
            break;
        }

        // Apply friend name if slide title doesn't exist.
        title = slide.title;
        if (title === undefined) {
            title = slide.name;
        }

        // Modify the link to bust the cache.
        cache = slide.cache;
        if (cache === undefined) {
            cache = self.cache;
        }
        if (cache !== 0) {
            date = Date.now();
            timestamp = Math.floor(date / 1000);
            if (cache > 0) {
                timestamp = Math.floor(date / 1000) -
                (Math.floor(date / 1000) % cache);
            }
            if (src.indexOf(separator) > -1) {
                separator = '&';
            }
            src += separator + 'time=' + timestamp;
        }

        // Update widget template.
        switch (slide.type) {
        case 'entity':
        case 'image':
            self.set_field(self, 'frame_src', '');
            self.set_field(self, 'img_internal_style', '');
            self.set_field(self, 'img_src', src);
            break;

        case 'url':
            self.set_field(self, 'frame_src', src);
            self.set_field(self, 'img_internal_style', 'display: none;');
            self.set_field(self, 'img_src', '/images/Blank.gif');
            break;
        }
        self.set_field(self, 'title', title);

        // Iterate array position.
        self.index = self.index + 1;
        if (self.index === _slides.length) {
            self.index = 0;
        }

        // Wait a few seconds.
        delay = slide.delay;
        if (delay <= 0) {
            delay = self.delay;
        }
        clearTimeout(self.timeout);
        self.timeout = setTimeout(
            function() {
                refresh_frame(self);
            },
            delay * 1000
        );
    }
    refresh_frame(self);
}
