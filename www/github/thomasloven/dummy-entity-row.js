let HuiGenericEntityRow = customElements.get('hui-generic-entity-row')
class DummyEntityRow extends HuiGenericEntityRow {
  setConfig(config) {this.config = config;}
}
customElements.define('dummy-entity-row', DummyEntityRow);
