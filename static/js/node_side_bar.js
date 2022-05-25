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
    "#nsb_experience_base",
    "#nsb_proficiency_menu",
    "#nsb_proficiency_arrow",
    "#nsb_proficiency_toggle",
    "#nsb_proficiency_list",
    "#nsb_save_proficiency"
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

    this._nsb_elements["nsb_proficiency_toggle"].click(this._toggle_proficiency_menu.bind(this))
    
    this._nsb_elements["nsb_proficiency_list"].children().click(this._set_new_proficiency.bind(this));

    this._nsb_elements["nsb_save_proficiency"].click(this._save_proficiency.bind(this));

    $.valHooks.textarea = {
      get(el) {
        return el.value.replace(/\r?\n/g, "\r\n")
      }
    }

    this._description = this._nsb_elements["nsb_description"].val();
    this._current_info = null;
    this._proficiency_total = 5;
    this._proficiency = 0;
    // track changes in proficiency, prevent submittion of form if selected proficiency is the same as orignal
    this._original_proficiency = this._proficiency; 
    this._proficiency_levels = [
      "Aiming to Learn",
      "Some Understanding",
      "Some Proficiency",
      "Capable",
      "Able to Use Professionally",
      "Expert",
    ]

    this._nsb_elements["nsb_proficiency_bar"].width((this._proficiency/this._proficiency_total*100).toString()+"%")

    this.is_opened = false;

    // hide sidebar by default
    this.hide();
  }

  _toggle_proficiency_menu() {
    this._nsb_elements["nsb_proficiency_arrow"].toggleClass("rotate-180");
    this._nsb_elements["nsb_proficiency_menu"].toggleClass("scale-y-0");

    if (this._nsb_elements["nsb_proficiency_menu"].attr("data-active") === "true") {
      this._nsb_elements["nsb_proficiency_menu"].attr("data-active", "false")
    } else {
      this._nsb_elements["nsb_proficiency_menu"].attr("data-active", "true")
    }
  }

  _set_new_proficiency(e) {
    // `this` is not binded in this function to make accessing the selected profieciency easier.
    // `this` points to the li element that was clicked instead of the current class instance.
    const clicked_item = this._nsb_elements['nsb_proficiency_list'].find(e.target)
    const selected_proficiency = parseInt(clicked_item.attr("data-proficiency-value"))
    if (selected_proficiency === this._proficiency) 
      return;

    this._nsb_elements["nsb_save_proficiency"].removeClass("hidden")

    this._nsb_elements["nsb_proficiency_text"].text(clicked_item.attr("data-proficiency-text"))

    // update current node proficiency
    // setting a new length for the progress bar needs a reference to the current skill data.
    this._current_info.data.proficiency = selected_proficiency
    this._set_new_progress_length(this._current_info)
  }

  _save_proficiency() {
    if (this._original_proficiency === this._proficiency) {}
  }

  _get_form() {

    const form_data = new FormData(this._nsb_elements["nsb_description_form"][0]);
    form_data.append("skill_name", this._current_info.data.name)
    form_data.append("proficiency", this._proficiency.toString())

    const obj = {
      body: form_data,
      url: this._nsb_elements["nsb_description_form"].attr("action"),
      method: this._nsb_elements["nsb_description_form"].attr("method"),
    }

    return obj;
  }

  _submit_description(e) {
    e.preventDefault();
    const form = this._get_form();

    fetch(form.url, {
      method: form.method,
      body: form.body
    })
      .then((res) => {
        if (res.status === 200) {
          // update the node description data to the updated description once we get
          // a successful status.
          this._current_info.data.description = this._description;
        }
      })
      .catch(e => console.error(e)) // todo: show update failed message to user
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
    this._proficiency = node.data.proficiency ?? 0;
    this._nsb_elements["nsb_proficiency_bar"].width((this._proficiency/this._proficiency_total*100).toString()+"%")
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

    // close the proficiency menu if is active when updating content.
    if (this._nsb_elements["nsb_proficiency_menu"].attr("data-active") === "true") {
      this._toggle_proficiency_menu()
    }
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
