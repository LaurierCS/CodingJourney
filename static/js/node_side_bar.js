class NodeSideBar {
  NODE_SIDE_BAR_IDS = [
    "#nsb_image",
    "#nsb_name",
    "#nsb_close",
    "#nsb_proficiency_text",
    "#nsb_proficiency_bar",
    "#nsb_save_description",
    "#nsb_edit_description",
    "#nsb_description_form",
    "#nsb_description",
    "#nsb_experience_list",
  ];

  constructor(element_id) {
    if ($ === undefined)
      throw Error(
        "NodeSideBar: Please include JQuery for the sidebar to work."
      );

    // assert _element_id has to be a string.
    if (typeof element_id !== "string")
      throw Error(
        "NodeSideBar: Element ID has to be a string. Received " +
          typeof element_id
      );

    this._element_id = element_id ?? "nsb";

    this._nsb = $(`#${this._element_id}`);
    if (this._nsb.lenght < 1)
      throw Error("Could not find SideBar with id: " + this._element_id);

    this._nsb_elements = {}

    for (let id of this.NODE_SIDE_BAR_IDS) {
      let el = this._nsb.find(id)
      if (el.length > 0) {
        if (el.attr("id") === "nsb_close") {
          el.click((() => {
            this.hide()
          }).bind(this))
        }
        this._nsb_elements[id.replace("#", "")] = el
      } else {
        console.warn("NodeSideBar: Required element missing with id: " + id + " . Updating content related to that element won't be possible.")
      }
    }

    // hide sidebar by default
    this.hide();
  }

  updateContent(node) {
    if (node === undefined || node === null) {
      console.warn("NodeSideBar: Did not receive node content to update.");
      return;
    }
  }

  show() {
    if (!this._nsb.hasClass("translate-x-full")) {
      return;
    }

    this._nsb.removeClass("translate-x-full")
  }

  hide() {
    if (this._nsb.hasClass("translate-x-full")) {
      return;
    }
    this._nsb.addClass("translate-x-full")
  }
}
