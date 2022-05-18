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

    this._nsb_elements["nsb_close"].click(this.hide.bind(this));

    this._nsb_elements["nsb_edit_description"].click(this._toggle_description_edit.bind(this));

    this._nsb_elements["nsb_save_description"].click(this._save_description.bind(this));

    this._nsb_elements["nsb_description_form"].submit(this._submit_description.bind(this));

    $.valHooks.textarea = {
      get(el) {
        return el.value.replace(/\r?\n/g, "\r\n")
      }
    }

    this._description = this._nsb_elements["nsb_description"].val();
    this._current_info = null;
    this._profieciency_total = 5;
    this._profieciency = 0;

    this._nsb_elements["nsb_proficiency_bar"].width((this._profieciency/this._profieciency_total*100).toString()+"%")

    this.is_opened = false;

    // hide sidebar by default
    this.hide();
  }

  _submit_description(e) {
    e.preventDefault();
    const formData = new FormData(this._nsb_elements["nsb_description_form"][0]);
    const url = this._nsb_elements["nsb_description_form"].attr("action");

    formData.append("skill_name", this._current_info.data.name)

    fetch(url, {
      method: "POST",
      body: formData
    })
      .catch(e => console.error(e))
  }

  _save_description() {
    if (this._description !== this._nsb_elements["nsb_description"].val()) {
      // there is actual change, we make post request to update
      // the description in the database.
      // todo: make post request to update database
      this._description = this._nsb_elements["nsb_description"].val()

      this._nsb_elements["nsb_description_form"].submit()
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

  _create_experiences(node) {
    if (this._nsb_elements["nsb_experience_list"].children().length > 0) {
      // clean children
      this._nsb_elements["nsb_experience_list"].children().remove();
    }

    if (!node.data.experiences) return;

    for (let i=0;i<node.data.experiences.length;i++) {
      let clone = this._nsb_elements["nsb_experience_base"].clone()
      clone.removeClass("hidden")
      clone
        .find("#nsb_experience_name")
        .text(node.data.experiences[i].name)
        .attr("id", `nsb_experience_index_${node.data.experiences[i].id}`)
      
      clone
        .find("#nsb_experience_link")
        .attr("data-experience-id", node.data.experiences[i].id)
        .attr("data-experience-href", node.data.experiences[i].project_link)
        .attr("href", node.data.experiences[i].project_link)
        .attr("id", `nsb_experience_link_${node.data.experiences[i].id}`)
      this._nsb_elements["nsb_experience_list"].append(clone);
    }
  }

  _set_new_progress_length(node) {
    this._profieciency = node.data.proficiency ?? 0;
    this._nsb_elements["nsb_proficiency_bar"].width((this._profieciency/this._profieciency_total*100).toString()+"%")
  }

  update_content(node) {
    if (node === undefined || node === null) {
      console.warn("NodeSideBar: Did not receive node content to update.");
      return;
    }
    
    this._current_info = node;
    this._nsb_elements["nsb_image"].attr("src", "/" + node.data.icon_HREF)
    this._nsb_elements["nsb_name"].text(node.data.name)

    this._nsb_elements["nsb_description"].val(node.data.description)
    this._description = this._nsb_elements["nsb_description"].val()

    if (node.data.proficiency_text) {
      this._nsb_elements["nsb_proficiency_text"].text(node.data.proficiency_text)
    } else {
      this._nsb_elements["nsb_proficiency_text"].text("")
    }

    this._set_new_progress_length(node);

    // create experiences list
    this._create_experiences(node);
  }

  show(d) {
    if (d && d === this._current_info && this.is_opened) {
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
