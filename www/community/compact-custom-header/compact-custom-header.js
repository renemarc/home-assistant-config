export const LitElement = Object.getPrototypeOf(
  customElements.get("ha-panel-lovelace")
);

export const html = LitElement.prototype.html;

export const fireEvent = (node, type, detail, options) => {
  options = options || {};
  detail = detail === null || detail === undefined ? {} : detail;
  const event = new Event(type, {
    bubbles: options.bubbles === undefined ? true : options.bubbles,
    cancelable: Boolean(options.cancelable),
    composed: options.composed === undefined ? true : options.composed
  });
  event.detail = detail;
  node.dispatchEvent(event);
  return event;
};

export const defaultConfig = {
  header: true,
  menu: "show",
  notifications: "show",
  voice: "show",
  options: "show",
  clock_format: 12,
  clock_am_pm: true,
  clock_date: false,
  date_locale: false,
  disable: false,
  main_config: false,
  chevrons: false,
  redirect: true,
  background: "",
  hide_tabs: [],
  show_tabs: [],
  kiosk_mode: false,
  sidebar_swipe: true,
  sidebar_closed: false,
  tab_color: {},
  button_color: {}
};

if (!customElements.get("compact-custom-header")) {
  class CompactCustomHeader extends LitElement {
    static get properties() {
      return {
        config: {},
        hass: {},
        editMode: {},
        showUa: {}
      };
    }

    constructor() {
      super();
      this.firstRun = true;
      this.editMode = false;
    }

    static async getConfigElement() {
      await import("./compact-custom-header-editor.js?v=1.0.4b9");
      return document.createElement("compact-custom-header-editor");
    }

    static getStubConfig() {
      return {};
    }

    setConfig(config) {
      this.config = config;
    }

    updated() {
      if (this.config && this.hass && this.firstRun) {
        this.buildConfig();
      }
    }

    render() {
      if (!this.editMode) {
        return html``;
      }
      return html`
        ${this.renderStyle()}
        <ha-card>
          <svg viewBox="0 0 24 24">
            <path
              d="M12,7L17,12H14V16H10V12H7L12,7M19,
                      21H5A2,2 0 0,1 3,19V5A2,2 0 0,1 5,
                      3H19A2,2 0 0,1 21,5V19A2,2 0 0,1 19,
                      21M19,19V5H5V19H19Z"
            ></path>
          </svg>
          <h2>Compact Custom Header</h2>
        </ha-card>
      `;
    }

    renderStyle() {
      return html`
        <style>
          [hidden] {
            display: none;
          }
          h2 {
            margin: auto;
            padding: 20px;
            background-color: var(--primary-color);
            color: var(--text-primary-color);
          }
          svg {
            float: left;
            height: 30px;
            padding: 15px 5px 15px 15px;
            fill: var(--text-primary-color);
          }
          .user_agent {
            display: block;
            margin-left: auto;
            margin-right: auto;
            padding: 5px;
            border: 0;
            resize: none;
            width: 100%;
          }
        </style>
      `;
    }

    buildConfig() {
      if (window.location.href.includes("clear_cch_cache")) {
        localStorage.removeItem("cchCache");
        window.location.replace(
          window.location.href.replace("?clear_cch_cache", "")
        );
      }

      if (this.firstRun) {
        this.firstRun = false;
        this.userVars = {
          user: this.hass.user.name,
          user_agent: navigator.userAgent
        };
      }

      if (this.config.main_config) {
        let cache = this.config ? Object.assign({}, this.config) : null;
        delete cache.main_config;
        localStorage.setItem("cchCache", JSON.stringify(cache));
      } else if (localStorage.getItem("cchCache")) {
        this.config = JSON.parse(localStorage.getItem("cchCache"));
      }

      let exceptionConfig = {};
      let highestMatch = 0;
      if (this.config.exceptions) {
        this.config.exceptions.forEach(exception => {
          const matches = this.countMatches(exception.conditions);
          if (matches > highestMatch) {
            highestMatch = matches;
            exceptionConfig = exception.config;
          }
        });
      }

      this.cchConfig = {
        ...defaultConfig,
        ...this.config,
        ...exceptionConfig
      };

      this.run();
    }

    countMatches(conditions) {
      let count = 0;
      for (const condition in conditions) {
        if (
          this.userVars[condition] == conditions[condition] ||
          (condition == "user_agent" &&
            this.userVars[condition].includes(conditions[condition])) ||
          (condition == "media_query" &&
            window.matchMedia(conditions[condition]).matches)
        ) {
          count++;
        } else {
          return 0;
        }
      }
      return count;
    }

    getCardSize() {
      return 0;
    }

    run() {
      const root = this.rootElement;
      const header = root.querySelector("app-header");
      const buttons = this.getButtonElements(root);
      const tabContainer = root.querySelector("paper-tabs");
      const tabs = tabContainer
        ? Array.from(tabContainer.querySelectorAll("paper-tab"))
        : [];
      const view = root
        .querySelector("ha-app-layout")
        .querySelector('[id="view"]');
      this.editMode =
        root.querySelector("app-toolbar").className == "edit-mode";
      let hidden_tabs;

      if (!this.editMode) this.hideCard();
      if (this.editMode && !this.cchConfig.disable) {
        this.removeStyles(tabContainer, header, view, root, tabs);
        if (buttons.options) this.insertEditMenu(buttons.options, tabs);
      } else if (
        !this.cchConfig.disable &&
        !window.location.href.includes("disable_cch")
      ) {
        this.styleButtons(buttons, tabs, root);
        this.styleHeader(root, tabContainer, header, view, tabs);
        if (this.cchConfig.hide_tabs && tabContainer) {
          hidden_tabs = this.hideTabs(tabContainer, tabs);
        }
        this.restoreTabs(tabs, hidden_tabs);
        this.defaultTab(tabs, tabContainer);

        for (const button in buttons) {
          if (this.cchConfig[button] == "clock") {
            this.insertClock(
              buttons,
              buttons[button].querySelector("paper-icon-button")
                ? buttons[button]
                : buttons[button].shadowRoot
            );
          }
        }

        const conditionals = this.cchConfig.conditional_styles;
        const monitorNotifications = () => {
          for (const key in conditionals) {
            if (conditionals[key].entity == "notifications") return true;
          }
          return false;
        };
        if (conditionals && !this.editMode) {
          this.conditionalStyling(header, buttons, tabs, root);
          if (monitorNotifications) {
            this.notifMonitor(header, buttons, tabs, root);
          }
          this.hass.connection.socket.addEventListener("message", event => {
            if (root.querySelector("app-toolbar").className != "edit-mode") {
              this.conditionalStyling(header, buttons, tabs, root);
            }
          });
        }

        if (this.cchConfig.swipe) {
          this.swipeNavigation(root, tabs, tabContainer, view);
        }
        this.sidebarMod(buttons);
        if (!this.editMode) this.tabContainerMargin(buttons, tabContainer);
        fireEvent(this, "iron-resize");
      }
    }

    tabContainerMargin(buttons, tabContainer) {
      let marginRight = 0;
      let marginLeft = 15;
      for (const button in buttons) {
        if (
          this.cchConfig[button] == "show" &&
          buttons[button].style.display !== "none"
        ) {
          if (button == "menu") {
            marginLeft += 45;
          } else {
            marginRight += 45;
          }
        } else if (
          this.cchConfig[button] == "clock" &&
          buttons[button].style.display !== "none"
        ) {
          const clockWidth =
            (this.cchConfig.clock_format == 12 && this.cchConfig.clock_am_pm) ||
            this.cchConfig.clock_date
              ? 90
              : 80;
          if (button == "menu") {
            marginLeft += clockWidth + 15;
          } else {
            marginRight += clockWidth;
          }
        }
      }
      if (tabContainer) {
        tabContainer.style.marginRight = marginRight + "px";
        tabContainer.style.marginLeft = marginLeft + "px";
      }
    }

    get rootElement() {
      try {
        let panelResolver = document
          .querySelector("home-assistant")
          .shadowRoot.querySelector("home-assistant-main")
          .shadowRoot.querySelector("app-drawer-layout partial-panel-resolver");
        if (panelResolver.shadowRoot) {
          return panelResolver.shadowRoot
            .querySelector("ha-panel-lovelace")
            .shadowRoot.querySelector("hui-root").shadowRoot;
        } else {
          return document
            .querySelector("home-assistant")
            .shadowRoot.querySelector("home-assistant-main")
            .shadowRoot.querySelector("ha-panel-lovelace")
            .shadowRoot.querySelector("hui-root").shadowRoot;
        }
      } catch (e) {
        console.log("Can't find 'hui-root', going to walk the DOM to find it.");
      }
      this.recursiveWalk(document, "HUI-ROOT", node => {
        return node.nodeName == "HUI-ROOT" ? node.shadowRoot : null;
      });
    }

    insertEditMenu(optionsBtn, tabs) {
      if (this.cchConfig.hide_tabs) {
        let show_tabs = document.createElement("paper-item");
        show_tabs.setAttribute("id", "show_tabs");
        show_tabs.addEventListener("click", () => {
          for (let i = 0; i < tabs.length; i++) {
            tabs[i].style.removeProperty("display");
          }
        });
        show_tabs.innerHTML = "Show all tabs";
        this.insertMenuItem(
          optionsBtn.querySelector("paper-listbox"),
          show_tabs
        );
      }
    }

    getButtonElements(root) {
      const buttons = {};
      buttons.options = root.querySelector("paper-menu-button");

      if (!this.editMode) {
        buttons.menu = root.querySelector("ha-menu-button");
        buttons.voice = root.querySelector("ha-start-voice-button");
        buttons.notifications = root.querySelector("hui-notifications-button");
      }
      return buttons;
    }

    removeStyles(tabContainer, header, view, root, tabs) {
      let header_colors = root.querySelector('[id="cch_header_colors"]');
      if (tabContainer) {
        tabContainer.style.marginLeft = "";
        tabContainer.style.marginRight = "";
      }
      header.style.background = null;
      view.style.marginTop = "0px";
      view.querySelectorAll("*")[0].style.display = "initial";
      if (root.querySelector('[id="cch_iron_selected"]')) {
        root.querySelector('[id="cch_iron_selected"]').outerHTML = "";
      }
      if (header_colors) header_colors.parentNode.removeChild(header_colors);
      for (let i = 0; i < tabs.length; i++) {
        tabs[i].style.color = "";
      }
    }

    styleHeader(root, tabContainer, header, view, tabs) {
      if (
        (!this.cchConfig.header && !this.editMode) ||
        this.cchConfig.kiosk_mode
      ) {
        header.style.display = "none";
      } else if (!this.editMode) {
        view.style.marginTop = "-48.5px";
        if (view.querySelector("hui-view")) {
          view.querySelector("hui-view").style.paddingTop = "55px";
        } else {
          view.querySelectorAll("*")[0].style.paddingTop = "55px";
          view.querySelectorAll("*")[0].style.display = "block";
        }
        let cchThemeBg = getComputedStyle(document.body).getPropertyValue(
          "--cch-background"
        );
        header.style.background =
          this.cchConfig.background || cchThemeBg || "var(--primary-color)";
      }
      view.style.minHeight = "100vh";

      // Add top margin to unused-entities page.
      if (!view.parentNode.querySelector('[id="cch_unused"]')) {
        let style = document.createElement("style");
        style.setAttribute("id", "cch_unused");
        style.innerHTML = `
          hui-unused-entities {
            display: inline-block;
            padding-top:50px;
          }
        `;
        view.parentNode.appendChild(style);
      }

      // Style all icons, all tab icons, and selection indicator.
      let indicator = this.cchConfig.tab_indicator_color;
      let all_tabs_color =
        this.cchConfig.all_tabs_color || "var(--cch-all-tabs-color)";
      if (
        indicator &&
        !root.querySelector('[id="cch_header_colors"]') &&
        !this.editMode
      ) {
        let style = document.createElement("style");
        style.setAttribute("id", "cch_header_colors");
        style.innerHTML = `
          paper-tabs {
            ${
              indicator
                ? `--paper-tabs-selection-bar-color: ${indicator} !important`
                : "var(--cch-tab-indicator-color) !important"
            }
          }
        `;
        root.appendChild(style);
      }

      // Style active tab icon color.
      let conditionalTabs = this.cchConfig.conditional_styles
        ? JSON.stringify(this.cchConfig.conditional_styles).includes("tab")
        : false;
      if (
        !root.querySelector('[id="cch_iron_selected"]') &&
        !this.editMode &&
        !conditionalTabs &&
        tabContainer
      ) {
        let style = document.createElement("style");
        style.setAttribute("id", "cch_iron_selected");
        style.innerHTML = `
            .iron-selected {
              ${
                this.cchConfig.active_tab_color
                  ? `color: ${this.cchConfig.active_tab_color + " !important"}`
                  : "var(--cch-active-tab-color)"
              }
            }
          `;
        tabContainer.appendChild(style);
      }

      // Style tab icon color.
      if (
        this.cchConfig.tab_color &&
        Object.keys(this.cchConfig.tab_color).length
      ) {
        for (let i = 0; i < tabs.length; i++) {
          tabs[i].style.color = this.cchConfig.tab_color[i] || all_tabs_color;
        }
      }

      if (tabContainer) {
        // Shift the header up to hide unused portion.
        root.querySelector("app-toolbar").style.marginTop = "-64px";

        if (!this.cchConfig.chevrons) {
          // Hide chevrons.
          let chevron = tabContainer.shadowRoot.querySelectorAll(
            '[icon^="paper-tabs:chevron"]'
          );
          chevron[0].style.display = "none";
          chevron[1].style.display = "none";
        } else {
          // Remove space taken up by "not-visible" chevron.
          let style = document.createElement("style");
          style.setAttribute("id", "cch_chevron");
          style.innerHTML = `
            .not-visible {
              display:none;
            }
          `;
          tabContainer.shadowRoot.appendChild(style);
        }
      }
    }

    styleButtons(buttons, tabs, root) {
      let topMargin = tabs.length > 0 ? "margin-top:111px;" : "";
      for (const button in buttons) {
        if (button == "options" && this.cchConfig[button] == "overflow") {
          this.cchConfig[button] = "show";
        }
        if (
          this.cchConfig[button] == "show" ||
          this.cchConfig[button] == "clock"
        ) {
          buttons[button].style.cssText = `
              z-index:1;
              ${topMargin}
              ${button == "options" ? "margin-right:-5px; padding:0;" : ""}
            `;
        } else if (this.cchConfig[button] == "overflow") {
          const paperIconButton = buttons[button].querySelector(
            "paper-icon-button"
          )
            ? buttons[button].querySelector("paper-icon-button")
            : buttons[button].shadowRoot.querySelector("paper-icon-button");
          if (paperIconButton.hasAttribute("hidden")) {
            continue;
          }
          const menu_items = buttons.options.querySelector("paper-listbox");
          const id = `menu_item_${button}`;
          if (!menu_items.querySelector(`[id="${id}"]`)) {
            const wrapper = document.createElement("paper-item");
            wrapper.setAttribute("id", id);
            wrapper.innerText = this.getTranslation(button);
            wrapper.appendChild(buttons[button]);
            wrapper.addEventListener("click", () => {
              paperIconButton.click();
            });
            paperIconButton.style.pointerEvents = "none";
            this.insertMenuItem(menu_items, wrapper);
            if (button == "notifications") {
              let style = document.createElement("style");
              style.innerHTML = `
                .indicator {
                  top: 5px;
                  right: 0px;
                  width: 10px;
                  height: 10px;
                  ${
                    this.cchConfig.notify_indicator_color
                      ? `background-color:${
                          this.cchConfig.notify_indicator_color
                        }`
                      : ""
                  }
                }
                .indicator > div{
                  display:none;
                }
              `;
              paperIconButton.parentNode.appendChild(style);
            }
          }
        } else if (this.cchConfig[button] == "hide") {
          buttons[button].style.display = "none";
        }
      }

      // Use button colors vars set in HA theme.
      buttons.menu.style.color = "var(--cch-button-color-menu)";
      buttons.notifications.style.color =
        "var(--cch-button-color-notifications)";
      buttons.voice.style.color = "var(--cch-button-color-voice)";
      buttons.options.style.color = "var(--cch-button-color-options)";
      if (this.cchConfig.all_buttons_color) {
        root.querySelector("app-toolbar").style.color =
          this.cchConfig.all_buttons_color || "var(--cch-all-buttons-color)";
      }

      // Use button colors set in config.
      for (const button in buttons) {
        if (this.cchConfig.button_color[button]) {
          buttons[button].style.color = this.cchConfig.button_color[button];
        }
      }

      if (
        this.cchConfig.notify_indicator_color &&
        this.cchConfig.notifications == "show"
      ) {
        let style = document.createElement("style");
        style.innerHTML = `
          .indicator {
            background-color:${this.cchConfig.notify_indicator_color ||
              "var(--cch-notify-indicator-color)"} !important;
            color: ${this.cchConfig.notify_text_color ||
              "var(--cch-notify-text-color), var(--primary-text-color)"};
          }
        `;
        buttons.notifications.shadowRoot.appendChild(style);
      }
    }

    getTranslation(button) {
      switch (button) {
        case "notifications":
          return this.hass.localize("ui.notification_drawer.title");
        default:
          return button.charAt(0).toUpperCase() + button.slice(1);
      }
    }

    defaultTab(tabs, tabContainer) {
      if (this.cchConfig.default_tab && !window.cchDefaultTab) {
        let default_tab = this.cchConfig.default_tab;
        let activeTab = tabs.indexOf(
          tabContainer.querySelector(".iron-selected")
        );
        if (
          activeTab != default_tab &&
          activeTab == 0 &&
          !this.cchConfig.hide_tabs.includes(default_tab)
        ) {
          tabs[default_tab].click();
        }
        window.cchDefaultTab = true;
      }
    }

    sidebarMod(buttons) {
      let menu = buttons.menu.querySelector("paper-icon-button");
      let sidebar = document
        .querySelector("home-assistant")
        .shadowRoot.querySelector("home-assistant-main")
        .shadowRoot.querySelector("app-drawer");
      if (!this.cchConfig.sidebar_swipe || this.cchConfig.kiosk_mode) {
        sidebar.removeAttribute("swipe-open");
      }
      if (
        (this.cchConfig.sidebar_closed || this.cchConfig.kiosk_mode) &&
        !window.cchSidebarClosed
      ) {
        if (sidebar.hasAttribute("opened")) menu.click();
        window.cchSidebarClosed = true;
      }
    }

    // Restore hidden tabs if config has changed.
    restoreTabs(tabs, hidden_tabs) {
      for (let i = 0; i < tabs.length; i++) {
        let hidden = hidden_tabs.includes(i);
        if (tabs[i].style.display == "none" && !hidden) {
          tabs[i].style.removeProperty("display");
        }
      }
    }

    hideTabs(tabContainer, tabs) {
      let hidden_tabs = String(this.cchConfig.hide_tabs).length
        ? String(this.cchConfig.hide_tabs)
            .replace(/\s+/g, "")
            .split(",")
        : null;
      let shown_tabs = String(this.cchConfig.show_tabs).length
        ? String(this.cchConfig.show_tabs)
            .replace(/\s+/g, "")
            .split(",")
        : null;

      // Set the tab config source.
      if (!hidden_tabs && shown_tabs) {
        let all_tabs = [];
        shown_tabs = this.buildRanges(shown_tabs);
        for (let i = 0; i < tabs.length; i++) all_tabs.push(i);
        // Invert shown_tabs to hidden_tabs.
        hidden_tabs = all_tabs.filter(el => !shown_tabs.includes(el));
      } else {
        hidden_tabs = this.buildRanges(hidden_tabs);
      }

      // Hide tabs.
      for (const tab of hidden_tabs) {
        if (!tabs[tab]) continue;
        tabs[tab].style.display = "none";
      }

      if (this.cchConfig.redirect) {
        // Check if current tab is a hidden tab.
        const activeTab = tabContainer.querySelector("paper-tab.iron-selected");
        const activeTabIndex = tabs.indexOf(activeTab);
        if (
          hidden_tabs.includes(activeTabIndex) &&
          hidden_tabs.length != tabs.length
        ) {
          let i = 0;
          // Find the first visible tab and navigate.
          while (hidden_tabs.includes(i)) {
            i++;
          }
          tabs[i].click();
        }
      }
      return hidden_tabs;
    }

    // If this card is the only one in a column hide column outside edit mode.
    hideCard() {
      if (this.parentNode.children.length == 1) {
        this.parentNode.style.display = "none";
      }
      this.style.display = "none";
    }

    // Insert items into overflow menu.
    insertMenuItem(menu_items, element) {
      let first_item = menu_items.querySelector("paper-item");
      if (!menu_items.querySelector(`[id="${element.id}"]`)) {
        first_item.parentNode.insertBefore(element, first_item);
      }
    }

    insertClock(buttons, clock_button) {
      const clockIcon = clock_button.querySelector("paper-icon-button");
      const clockIronIcon = clockIcon.shadowRoot.querySelector("iron-icon");
      const clockWidth =
        (this.cchConfig.clock_format == 12 && this.cchConfig.clock_am_pm) ||
        this.cchConfig.clock_date
          ? 90
          : 80;

      if (
        this.cchConfig.notifications == "clock" &&
        this.cchConfig.clock_date &&
        !buttons.notifications.shadowRoot.querySelector('[id="cch_indicator"]')
      ) {
        let style = document.createElement("style");
        style.setAttribute("id", "cch_indicator");
        style.innerHTML = `
          .indicator {
            top: unset;
            bottom: -3px;
            right: 0px;
            width: 90%;
            height: 3px;
            border-radius: 0;
            ${
              this.cchConfig.notify_indicator_color
                ? `background-color:${this.cchConfig.notify_indicator_color}`
                : ""
            }
          }
          .indicator > div{
            display:none;
          }
        `;
        buttons.notifications.shadowRoot.appendChild(style);
      }

      let clockElement = clockIronIcon.parentNode.getElementById("cch_clock");
      if (!clockElement) {
        clockIcon.style.cssText = `
              margin-right:-5px;
              width:${clockWidth}px;
              text-align: center;
            `;

        clockElement = document.createElement("p");
        clockElement.setAttribute("id", "cch_clock");
        let clockAlign = "center";
        let padding = "";
        let fontSize = "";
        if (this.cchConfig.clock_date && this.cchConfig.menu == "clock") {
          clockAlign = "left";
          padding = "margin-right:-20px";
          fontSize = "font-size:12pt";
        } else if (this.cchConfig.clock_date) {
          clockAlign = "right";
          padding = "margin-left:-20px";
          fontSize = "font-size:12pt";
        }
        let marginTop = this.cchConfig.clock_date ? "-4px" : "2px";
        clockElement.style.cssText = `
              margin-top: ${marginTop};
              text-align: ${clockAlign};
              ${padding};
              ${fontSize};
            `;
        clockIronIcon.parentNode.insertBefore(clockElement, clockIronIcon);
        clockIronIcon.style.display = "none";
      }

      const clockFormat = {
        hour12: this.cchConfig.clock_format != 24,
        hour: "2-digit",
        minute: "2-digit"
      };
      this.updateClock(clockElement, clockFormat);
    }

    updateClock(clock, clockFormat) {
      let date = new Date();
      let locale = this.cchConfig.date_locale || this.hass.language;
      let time = date.toLocaleTimeString([], clockFormat);
      let options = {
        weekday: "short",
        month: "2-digit",
        day: "2-digit"
      };
      date = this.cchConfig.clock_date
        ? `</br>${date.toLocaleDateString(locale, options)}`
        : "";
      if (!this.cchConfig.clock_am_pm && this.cchConfig.clock_format == 12) {
        clock.innerHTML = time.slice(0, -3) + date;
      } else {
        clock.innerHTML = time + date;
      }
      window.setTimeout(() => this.updateClock(clock, clockFormat), 60000);
    }

    conditionalStyling(header, buttons, tabs, root) {
      if (window.cchState == undefined) window.cchState = [];
      if (this.prevColor == undefined) this.prevColor = {};
      if (this.prevState == undefined) this.prevState = [];
      const conditional_styles = this.cchConfig.conditional_styles;
      let tabContainer = tabs[0] ? tabs[0].parentNode : "";
      let elem, color, bg, hide, onIcon, offIcon, iconElem;

      const styleElements = (elem, color, hide, bg, onIcon, iconElem) => {
        if (bg && elem == "background") {
          header.style.background = bg;
        } else if (color) {
          elem.style.color = color;
        }
        if (onIcon && iconElem) iconElem.setAttribute("icon", onIcon);
        if (hide && elem !== "background" && !this.editMode) {
          elem.style.display = "none";
        }
      };

      const getElements = (key, elemArray, i, obj, styling) => {
        elem = elemArray[key];
        color = styling[i][obj][key].color;
        onIcon = styling[i][obj][key].on_icon;
        offIcon = styling[i][obj][key].off_icon;
        hide = styling[i][obj][key].hide;
        if (!this.prevColor[key]) {
          this.prevColor[key] = window
            .getComputedStyle(elem, null)
            .getPropertyValue("color");
        }
      };

      let styling = [];
      if (Array.isArray(conditional_styles)) {
        for (let i = 0; i < conditional_styles.length; i++) {
          styling.push(Object.assign({}, conditional_styles[i]));
        }
      } else {
        styling.push(Object.assign({}, conditional_styles));
      }

      for (let i = 0; i < styling.length; i++) {
        let template = styling[i].template;
        if (template) {
          if (!template.length) template = [template];
          for (let x = 0; x < template.length; x++) {
            this.templateConditional(template[x], header, buttons, tabs);
          }
          continue;
        }
        let entity = styling[i].entity;
        if (
          this.hass.states[entity] == undefined &&
          entity !== "notifications"
        ) {
          throw new Error(`${entity} does not exist.`);
        }
        if (entity == "notifications") {
          window.hassConnection.then(function(result) {
            window.cchState[i] = !!result.conn._ntf.state.length;
          });
        } else {
          window.hassConnection.then(function(result) {
            window.cchState[i] = result.conn._ent.state[entity].state;
          });
        }
        if (window.cchState[i] == undefined) {
          window.setTimeout(() => {
            if (root.querySelector("app-toolbar").className != "edit-mode") {
              this.conditionalStyling(header, buttons, tabs, root);
            }
          }, 100);
          return;
        }

        if (
          window.cchState[i] !== this.prevState[i] ||
          !window.cchState.length
        ) {
          this.prevState[i] = window.cchState[i];
          let above = styling[i].condition.above;
          let below = styling[i].condition.below;

          for (const obj in styling[i]) {
            let key;
            if (styling[i][obj]) {
              key = Object.keys(styling[i][obj])[0];
            }
            if (obj == "background") {
              elem = "background";
              color = styling[i][obj].color;
              bg = styling[i][obj];
              iconElem = false;
              if (!this.prevColor[obj]) {
                this.prevColor[obj] = window
                  .getComputedStyle(header, null)
                  .getPropertyValue("background");
              }
            } else if (obj == "button") {
              getElements(key, buttons, i, obj, styling);
              if (key == "menu") {
                iconElem = elem
                  .querySelector("paper-icon-button")
                  .shadowRoot.querySelector("iron-icon");
              } else {
                iconElem = elem.shadowRoot
                  .querySelector("paper-icon-button")
                  .shadowRoot.querySelector("iron-icon");
              }
            } else if (obj == "tab") {
              getElements(key, tabs, i, obj, styling);
              iconElem = elem.querySelector("ha-icon");
            }

            if (window.cchState[i] == styling[i].condition.state) {
              styleElements(elem, color, hide, bg, onIcon, iconElem);
            } else if (
              above !== undefined &&
              below !== undefined &&
              window.cchState[i] > above &&
              window.cchState[i] < below
            ) {
              styleElements(elem, color, hide, bg, onIcon, iconElem);
            } else if (
              above !== undefined &&
              below == undefined &&
              window.cchState[i] > above
            ) {
              styleElements(elem, color, hide, bg, onIcon, iconElem);
            } else if (
              above == undefined &&
              below !== undefined &&
              window.cchState[i] < below
            ) {
              styleElements(elem, color, hide, bg, onIcon, iconElem);
            } else {
              if (
                elem !== "background" &&
                hide &&
                elem.style.display == "none"
              ) {
                elem.style.display = "";
              }
              if (bg && elem == "background") {
                header.style.background = this.prevColor[obj];
              } else if (
                obj !== "background" &&
                obj !== "entity" &&
                obj !== "condition"
              ) {
                elem.style.color = this.prevColor[key];
              }
              if (onIcon && offIcon) {
                iconElem.setAttribute("icon", offIcon);
              }
            }
          }
        }
      }
      this.tabContainerMargin(buttons, tabContainer);
      fireEvent(this, "iron-resize");
    }

    templateConditional(template, header, buttons, tabs) {
      // Get entity states.
      window.hassConnection.then(function(result) {
        window.cchEntity = result.conn._ent.state;
      });
      if (!window.cchEntity) {
        window.setTimeout(() => {
          this.templateConditional(template, header, buttons, tabs);
        }, 100);
        return;
      }
      // Variables for templates.
      let states = window.cchEntity;
      let entity = window.cchEntity;

      const templateEval = (template, entity) => {
        try {
          if (template.includes("return")) {
            return eval(`(function() {${template}}())`);
          } else {
            return eval(template);
          }
        } catch (e) {
          console.log(e);
        }
      };

      for (const condition in template) {
        if (condition == "tab") {
          for (const tab in template[condition]) {
            if (!template[condition][tab].length) {
              template[condition][tab] = [template[condition][tab]];
            }
            for (let i = 0; i < template[condition][tab].length; i++) {
              let tabIndex = parseInt(Object.keys(template[condition]));
              let styleTarget = Object.keys(template[condition][tab][i]);
              let tempCond = template[condition][tab][i][styleTarget];
              if (styleTarget == "icon") {
                tabs[tabIndex]
                  .querySelector("ha-icon")
                  .setAttribute("icon", templateEval(tempCond, entity));
              } else if (styleTarget == "color") {
                tabs[tabIndex].style.color = templateEval(tempCond, entity);
              } else if (styleTarget == "display") {
                templateEval(tempCond, entity) == "show"
                  ? (tabs[tabIndex].style.display = "")
                  : (tabs[tabIndex].style.display = "none");
              }
            }
          }
        } else if (condition == "button") {
          for (const button in template[condition]) {
            if (!template[condition][button].length) {
              template[condition][button] = [template[condition][button]];
            }
            for (let i = 0; i < template[condition][button].length; i++) {
              let buttonName = Object.keys(template[condition]);
              let styleTarget = Object.keys(template[condition][button][i]);
              let buttonElem = buttons[buttonName];
              let iconTarget = buttonElem.shadowRoot
                ? buttonElem.shadowRoot.querySelector("paper-icon-button")
                : buttonElem.querySelector("paper-icon-button");
              let target = iconTarget.shadowRoot.querySelector("iron-icon");
              let tempCond = template[condition][button][i][styleTarget];
              if (styleTarget == "icon") {
                iconTarget.setAttribute("icon", templateEval(tempCond, entity));
              } else if (styleTarget == "color") {
                target.style.color = templateEval(tempCond, entity);
              } else if (styleTarget == "display") {
                templateEval(tempCond, entity) == "show"
                  ? (buttons[buttonName].style.display = "")
                  : (buttons[buttonName].style.display = "none");
              }
            }
          }
        } else if (condition == "background") {
          header.style.background = templateEval(template[condition], entity);
        }
      }
      entity = null;
    }

    // Use notification indicator element to monitor notification status.
    notifMonitor(header, buttons, tabs, root) {
      let notification = !!buttons.notifications.shadowRoot.querySelector(
        ".indicator"
      );
      if (window.cchNotification == undefined) {
        window.cchNotification = notification;
      } else if (notification !== window.cchNotification) {
        if (root.querySelector("app-toolbar").className != "edit-mode") {
          this.conditionalStyling(header, buttons, tabs, root);
        }
        window.cchNotification = notification;
      }
      window.setTimeout(
        () => this.notifMonitor(header, buttons, tabs, root),
        1000
      );
    }

    // Walk the DOM to find element.
    recursiveWalk(node, element, func) {
      let done = func(node) || node.nodeName == element;
      if (done) return true;
      if ("shadowRoot" in node && node.shadowRoot) {
        done = this.recursiveWalk(node.shadowRoot, element, func);
        if (done) return true;
      }
      node = node.firstChild;
      while (node) {
        done = this.recursiveWalk(node, element, func);
        if (done) return true;
        node = node.nextSibling;
      }
    }

    // Get range (e.g., "5 to 9") and build (5,6,7,8,9).
    buildRanges(array) {
      if (!array) array = [];
      const sortNumber = (a, b) => a - b;
      const range = (start, end) =>
        new Array(end - start + 1).fill(undefined).map((_, i) => i + start);

      for (let i = 0; i < array.length; i++) {
        if (array[i].length > 1 && array[i].includes("to")) {
          let split = array[i].split("to");
          array.splice(i, 1);
          array = array.concat(range(parseInt(split[0]), parseInt(split[1])));
        }
      }
      for (let i = 0; i < array.length; i++) array[i] = parseInt(array[i]);
      return array.sort(sortNumber);
    }

    swipeNavigation(root, tabs, tabContainer, view) {
      let swipe_amount = this.cchConfig.swipe_amount || 15;
      let animate = this.cchConfig.swipe_animate || "none";
      let skip_tabs = this.cchConfig.swipe_skip
        ? this.buildRanges(this.cchConfig.swipe_skip.split(","))
        : [];
      let wrap =
        this.cchConfig.swipe_wrap != undefined
          ? this.cchConfig.swipe_wrap
          : true;
      let prevent_default =
        this.cchConfig.swipe_prevent_default != undefined
          ? this.cchConfig.swipe_prevent_default
          : false;

      swipe_amount /= Math.pow(10, 2);
      const appLayout = root.querySelector("ha-app-layout");
      let xDown, yDown, xDiff, yDiff, activeTab, firstTab, lastTab, left;

      appLayout.addEventListener("touchstart", handleTouchStart, {
        passive: true
      });
      appLayout.addEventListener("touchmove", handleTouchMove, {
        passive: false
      });
      appLayout.addEventListener("touchend", handleTouchEnd, {
        passive: true
      });

      function handleTouchStart(event) {
        let ignored = ["APP-HEADER", "HA-SLIDER", "SWIPE-CARD", "HUI-MAP-CARD"];
        let path = (event.composedPath && event.composedPath()) || event.path;
        if (path) {
          for (let element of path) {
            if (element.nodeName == "HUI-VIEW") break;
            else if (ignored.indexOf(element.nodeName) > -1) return;
          }
        }
        xDown = event.touches[0].clientX;
        yDown = event.touches[0].clientY;
        if (!lastTab) filterTabs();
        activeTab = tabs.indexOf(tabContainer.querySelector(".iron-selected"));
      }

      function handleTouchMove(event) {
        if (xDown && yDown) {
          xDiff = xDown - event.touches[0].clientX;
          yDiff = yDown - event.touches[0].clientY;
          if (Math.abs(xDiff) > Math.abs(yDiff) && prevent_default) {
            event.preventDefault();
          }
        }
      }

      function handleTouchEnd() {
        if (activeTab < 0 || Math.abs(xDiff) < Math.abs(yDiff)) {
          xDown = yDown = xDiff = yDiff = null;
          return;
        }
        if (xDiff > Math.abs(screen.width * swipe_amount)) {
          left = false;
          activeTab == tabs.length - 1 ? click(firstTab) : click(activeTab + 1);
        } else if (xDiff < -Math.abs(screen.width * swipe_amount)) {
          left = true;
          activeTab == 0 ? click(lastTab) : click(activeTab - 1);
        }
        xDown = yDown = xDiff = yDiff = null;
      }

      function filterTabs() {
        tabs = tabs.filter(element => {
          return (
            !skip_tabs.includes(tabs.indexOf(element)) &&
            getComputedStyle(element, null).display != "none"
          );
        });
        firstTab = wrap ? 0 : null;
        lastTab = wrap ? tabs.length - 1 : null;
      }

      function click(index) {
        if (
          (activeTab == 0 && !wrap && left) ||
          (activeTab == tabs.length - 1 && !wrap && !left)
        ) {
          return;
        }
        if (animate == "swipe") {
          let _in = left
            ? `${screen.width / 1.5}px`
            : `-${screen.width / 1.5}px`;
          let _out = left
            ? `-${screen.width / 1.5}px`
            : `${screen.width / 1.5}px`;
          view.style.transitionDuration = "200ms";
          view.style.opacity = 0;
          view.style.transform = `translateX(${_in})`;
          view.style.transition = "transform 0.20s, opacity 0.20s";
          setTimeout(function() {
            tabs[index].dispatchEvent(
              new MouseEvent("click", { bubbles: false, cancelable: true })
            );
            view.style.transitionDuration = "0ms";
            view.style.transform = `translateX(${_out})`;
            view.style.transition = "transform 0s";
          }, 210);
          setTimeout(function() {
            view.style.transitionDuration = "200ms";
            view.style.opacity = 1;
            view.style.transform = `translateX(0px)`;
            view.style.transition = "transform 0.20s, opacity 0.20s";
          }, 215);
        } else if (animate == "fade") {
          view.style.transitionDuration = "200ms";
          view.style.transition = "opacity 0.20s";
          view.style.opacity = 0;
          setTimeout(function() {
            tabs[index].dispatchEvent(
              new MouseEvent("click", { bubbles: false, cancelable: true })
            );
            view.style.transitionDuration = "0ms";
            view.style.opacity = 0;
            view.style.transition = "opacity 0s";
          }, 210);
          setTimeout(function() {
            view.style.transitionDuration = "200ms";
            view.style.transition = "opacity 0.20s";
            view.style.opacity = 1;
          }, 250);
        } else if (animate == "flip") {
          view.style.transitionDuration = "200ms";
          view.style.transform = "rotatey(90deg)";
          view.style.transition = "transform 0.20s, opacity 0.20s";
          view.style.opacity = 0.25;
          setTimeout(function() {
            tabs[index].dispatchEvent(
              new MouseEvent("click", { bubbles: false, cancelable: true })
            );
          }, 210);
          setTimeout(function() {
            view.style.transitionDuration = "200ms";
            view.style.transform = "rotatey(0deg)";
            view.style.transition = "transform 0.20s, opacity 0.20s";
            view.style.opacity = 1;
          }, 250);
        } else {
          tabs[index].dispatchEvent(
            new MouseEvent("click", { bubbles: false, cancelable: true })
          );
        }
      }
    }
  }

  customElements.define("compact-custom-header", CompactCustomHeader);
}
