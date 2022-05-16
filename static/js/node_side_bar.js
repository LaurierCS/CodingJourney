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
    "#nsb_experience_base"
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
        this._nsb_elements[id.replace("#", "")] = el
      } else {
        console.warn("NodeSideBar: Required element missing with id: " + id + " . Updating content related to that element won't be possible.")
      }
    }

    this._nsb_elements["nsb_close"].click(this.hide.bind(this))

    this._nsb_elements["nsb_edit_description"].click(this._toggle_description_edit.bind(this));

    this._nsb_elements["nsb_save_description"].click(this._save_description.bind(this))

    $.valHooks.textarea = {
      get(el) {
        return el.value.replace(/\r?\n/g, "\r\n")
      }
    }

    this._description = this._nsb_elements["nsb_description"].val();
    this._currentInfo = null;

    this.is_opened = false;

    // hide sidebar by default
    this.hide();
  }

  _save_description() {
    if (this._description !== this._nsb_elements["nsb_description"].val()) {
      // there is actual change, we make post request to update
      // the description in the database.
      // todo: make post request to update database
      this._description = this._nsb_elements["nsb_description"].val()
    }

    this._toggle_description_edit();
  }

  _toggle_description_edit() {
    if (this._nsb_elements["nsb_description"].attr("readonly")) {
      this._nsb_elements["nsb_description"].removeAttr("readonly")
      this._nsb_elements["nsb_description"].focus()
      this._nsb_elements["nsb_save_description"].toggle()
    } else {
      // check if the description has changed or not
      if (this._description !== this._nsb_elements["nsb_description"].val() && !confirm("Quitting now will not save the changes. Are you sure?")) {
        return;
      }
      // if there were changes and the user confirm edit mode without
      // saving, then reset the description value and make the textarea readonly.
      this._nsb_elements["nsb_description"].val(this._description)
      this._nsb_elements["nsb_description"].attr("readonly", "true")
      this._nsb_elements["nsb_save_description"].toggle()
    }
  }

  _create_experiences(d) {
    if (this._nsb_elements["nsb_experience_list"].children().length > 0) {
      // clean children
      this._nsb_elements["nsb_experience_list"].children().remove();
    }

    for (let i=0;i<Math.floor(Math.random() * 20);i++) {
      let clone = this._nsb_elements["nsb_experience_base"].clone()
      clone.removeClass("hidden")
      clone
        .find("#nsb_experience_name")
        .text("Sample Experience Name")
        .attr("id", `nsb_experience_index_${i}`)
      this._nsb_elements["nsb_experience_list"].append(clone);
    }
  }

  update_content(node) {
    if (node === undefined || node === null) {
      console.warn("NodeSideBar: Did not receive node content to update.");
      return;
    }
    
    this._currentInfo = node;
    this._nsb_elements["nsb_image"].attr("src", "/" + node.data.icon_HREF)
    this._nsb_elements["nsb_name"].text(node.data.name)

    // todo: update the description
    // todo: update proficiencies

    // create experiences list
    this._create_experiences(node);
  }

  show(d) {
    if (d && d === this._currentInfo && this.is_opened) {
      return;
    }
    // update content first
    if (d) {
      this.update_content(d)
    }
    // show
    this._nsb.removeClass("translate-x-full")
    this.is_opened = true;
  }

  hide() {
    if (this._nsb.hasClass("translate-x-full")) {
      return;
    }
    this._nsb.addClass("translate-x-full")
    this.is_opened = false;
  }
}
