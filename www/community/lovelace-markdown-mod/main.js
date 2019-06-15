import {html} from "/card-tools/lit-element.js";
import {parseTemplate} from "/card-tools/templates.js";
import {fireEvent} from "/card-tools/event.js";

customElements.whenDefined('ha-markdown').then(() => {
  const HaMarkdown = customElements.get('ha-markdown');

  // Patch ha-markdown.filterXSS to allow ha-icon tags
  // filterXSS is lazy-loaded, so we need to patch it in the _render function
  const svgWhiteList = ["svg", "path", "ha-icon"];
  const oldRender = HaMarkdown.prototype._render;
  HaMarkdown.prototype._render = function () {
    if (this._scriptLoaded === 0 || this._renderScheduled) return;
    if(! this.oldFilterXSS) {
      this.oldFilterXSS = this.filterXSS;
    }
    this.filterXSS = function(data, options) {
      if(data == -1) return 1;
      return this.oldFilterXSS(data, {
        onIgnoreTag: this.allowSvg
        ? (tag, html) => (svgWhiteList.indexOf(tag) >= 0 ? html: null)
        : null,
      });
    }
    oldRender.bind(this)();
  };
  // Rebuild everything to make sure the patched versions are loaded
  fireEvent('ll-rebuild', {});
});


customElements.whenDefined('hui-markdown-card').then(() => {
  const HuiMarkDownCard = customElements.get('hui-markdown-card');

  // Change content of ha-markdown element and allow svgs after each update
  HuiMarkDownCard.prototype.updated = function(_) {
    const markdown = this.shadowRoot.querySelector("ha-markdown");
    if(!markdown) return;
    markdown.allowSvg = true;
    markdown.content = parseTemplate(this._config.content);
  }

  // Add a listener for location-changed on first update
  // This helps keeping track of the page hash
  HuiMarkDownCard.prototype.firstUpdated = function () {
    window.addEventListener("location-changed", () => this._requestUpdate());
  }

  // Add a .hass property to hui-markdown-card and update when it's changed
  Object.defineProperty(HuiMarkDownCard.prototype, 'hass', {
    get() {
      return this._hass;
    },
    set(value) {
      if(value !== this._hass) {
        const oldval = this._hass;
        this._hass = value;
        this._requestUpdate('hass', oldval);
      }
    },
  });
  // Rebuild everything to make sure the patched versions are loaded
  fireEvent('ll-rebuild', {});
});
