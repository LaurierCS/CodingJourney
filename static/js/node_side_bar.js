class NodeSideBar {
  NODE_SIDE_BAR_IDS = [
    "#nsb_image",
    "#nsb_name",
    "#nsb_close",
    "#nsb_proficiency_text",
    "#nsb_proficiency_bar",
    "#nsb_save",
    "#nsb_edit",
    "#nsb_description_form",
    "#nsb_description",
    "#nsb_experience_list",
    "#nsb_experience_base",
    "#nsb_proficiency_menu",
    "#nsb_proficiency_arrow",
    "#nsb_proficiency_toggle",
    "#nsb_proficiency_list",
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

    this._nsb_elements["nsb_edit"].click(this._toggle_edit.bind(this));

    this._nsb_elements["nsb_save"].click(this._save.bind(this));

    this._nsb_elements["nsb_description_form"].submit(this._submit_changes.bind(this));

    this._nsb_elements["nsb_proficiency_toggle"].click(this._toggle_proficiency_menu.bind(this))
    
    this._nsb_elements["nsb_proficiency_list"].children().click(this._onselect_proficiency.bind(this));

    $.valHooks.textarea = {
      get(el) {
        return el.value.replace(/\r?\n/g, "\r\n")
      }
    }

    this._description = this._nsb_elements["nsb_description"].val();

    // points to the current node data, same object as a descendant from the tree data.
    this._current_info = null;
    
    // track changes in proficiency, prevent submittion of form if selected proficiency is the same as orignal
    this._proficiency = 0;
    this._original_proficiency = this._proficiency;
    this._proficiency_text = this._nsb_elements["nsb_proficiency_text"].text();
    this._original_proficiency_text = this._proficiency_text;
    this._proficiency_total = 5;

    this._proficiency_levels = [
      "Aiming to Learn",
      "Some Understanding",
      "Some Proficiency",
      "Capable",
      "Able to Use Professionally",
      "Expert",
    ]

    this._set_new_progress_length(this._proficiency)

    this.is_opened = false;
    this.is_editable = false;

    // hide sidebar by default
    this.hide();
  }

  /**
   * Toggles the proficiency menu.
   * @returns 
   */
  _toggle_proficiency_menu() {

    if (!this.is_editable) return;

    // toggle animation
    this._nsb_elements["nsb_proficiency_arrow"].toggleClass("rotate-180");
    this._nsb_elements["nsb_proficiency_menu"].toggleClass("scale-y-0");

    if (this._nsb_elements["nsb_proficiency_menu"].attr("data-active") === "true") {
      this._nsb_elements["nsb_proficiency_menu"].attr("data-active", "false")
    } else {
      this._nsb_elements["nsb_proficiency_menu"].attr("data-active", "true")
    }
  }

  /**
   * Updates the proficiency text and proficiency bar when a new proficiency is selected.
  * ! THIS METHOD DOES NOT SUBMIT ANY DATA TO THE BACKEND FOR UPDATE !
   * @param {Event} e 
   * @returns 
   */
  _onselect_proficiency(e) {
    const clicked_item = this._nsb_elements['nsb_proficiency_list'].find(e.target)
    const selected_proficiency = parseInt(clicked_item.attr("data-proficiency-value"))
    
    // same proficiency
    if (selected_proficiency === this._proficiency) 
      return;

    this._set_proficiency_text(clicked_item.attr("data-proficiency-text"))
    this._set_new_progress_length(selected_proficiency)
  }

  /**
   * Construct a valid form for submission.
   * @returns {{body: FormData, url: string, method: string}}
   */
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

  /**
   * Submits form with new values to backend.
   * Will reset description and proficiency on fail.
   * @param {Event} e 
   */
  _submit_changes(e) {
    e.preventDefault();
    const form = this._get_form();

    fetch(form.url, {
      method: form.method,
      body: form.body
    })
      .then((res) => res.json())
      .then((new_data) => {
        // update the node description data to the updated description once we get
        // a successful status.
        this._description = new_data.description;
        this._current_info.data.description = this._description;
        this._current_info.data.proficiency = new_data.proficiency;
        this._current_info.data.proficiency_text = new_data.proficiency_text;
        this._original_proficiency = this._set_new_progress_length(new_data.proficiency)
        this._original_proficiency_text = this._set_proficiency_text(new_data.proficiency_text)
        
        this._toggle_edit();
      })
      .catch(e => {
        console.error(e)
        
        // reset all values
        this._reset_values();

        // todo: show update failed message to user
      });
  }

  /**
   * Triggers submit event of form if changes detected.
   */
  _save() {
    // only submit if there was actual change
    if (this._has_changes()) {
      this._nsb_elements["nsb_description_form"].submit()
    }
  }

  /**
   * Toggles edit mode.
   * Will ask for confirmation before toggle if changes detected.
   * Toggle is not ensured because user can cancel toggle when ask for confirmation to exit without saving.
   * @returns {boolean} true if edit mode was toggled successfully, false otherwise.
   */
  _toggle_edit() {
    if (this._nsb_elements["nsb_description"].attr("readonly") && !this.is_editable) {
      this._nsb_elements["nsb_description"].removeAttr("readonly")
      this._nsb_elements["nsb_description"].focus()
    } else {
      // check if the description has changed or not
      if (this._has_changes() && !this._confirm_exit()) {
        return false;
      }
      // if there were changes and the user confirm edit mode without
      // saving, then reset all values
      this._reset_values();
    }
    
    this._nsb_elements["nsb_save"].toggle()
    this._nsb_elements["nsb_proficiency_arrow"].toggleClass("hidden");
    this._nsb_elements["nsb_proficiency_toggle"].toggleClass("cursor-pointer")
    this.is_editable = !this.is_editable;

    return true;
  }

  /**
   * Resets all fields.
   */
  _reset_values() {
    this._nsb_elements["nsb_description"].val(this._description);
    this._nsb_elements["nsb_description"].attr("readonly", "true");

    this._set_proficiency_text(this._original_proficiency_text);
    this._set_new_progress_length(this._original_proficiency);
  }

  /**
   * Creates a list of experiences of the selected skill.
   * Elements are auto appended into the DOM.
   * @param {descendant} node A descendant object from d3.js 
   * @returns 
   */
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

  /**
   * Sets the progress bar under the proficiency section.
   * Updates the property `this._proficiency` as well.
   * @param {descendant|number} node_or_number A descendant object(from d3.js) or a number
   * @returns 
   */
  _set_new_progress_length(node_or_number) {
    if (typeof node_or_number === "number") {
      this._proficiency = node_or_number;
    } else {
      this._proficiency = node_or_number.data.proficiency ?? 0;
    }

    this._nsb_elements["nsb_proficiency_bar"].width((this._proficiency/this._proficiency_total*100).toString()+"%")

    return this._proficiency;
  }

  /**
   * Sets the text for the proficiency.
   * Updates the property `this._proficiency_text` as well.
   * @param {descendant|string} node_or_text A descedant object(from d3.js) or a string
   * @returns {string}
   */
  _set_proficiency_text(node_or_text) {
    if (typeof node_or_text === "string") {
      this._proficiency_text = node_or_text;
    } else {
      this._proficiency_text = node_or_text.data.proficiency_text ?? "";
    }

    this._nsb_elements["nsb_proficiency_text"].text(this._proficiency_text);

    return this._proficiency_text;
  }

  /**
   * Check if the description or proficiency has changed.
   * @returns {boolean}
   */
  _has_changes() {
    return this._description !== this._nsb_elements["nsb_description"].val() || this._original_proficiency !== this._proficiency
  }

  /**
   * Creates an alert popup asking if the user wants to exit without saving.
   * @returns {boolean}
   */
  _confirm_exit() {
    return confirm("Quitting now will not save the changes. Are you sure?");
  }

  /**
   * Updates the contents of the side bar.
   * @param {descendant} node A descendant object from d3.js 
   * @returns 
   */
  update_content(node) {
    if (node === undefined || node === null) {
      console.warn("NodeSideBar: Did not receive node content to update.");
      return;
    }

    /**
     * A user can click on another skill while the sidebar is opened and in edit mote.
     * In this case, we want to close edit mode before updating any content.
     * This ensures that any changes that the user was making is not lost by misclicking another skill on the tree.
     */
    if (this.is_editable && !this._toggle_edit()) return;
    
    this._current_info = node;
    // this._nsb_elements["nsb_image"].attr("src", "/" + node.data.icon_HREF)
    this._nsb_elements["nsb_image"].attr("src", "/static/images/svg/badge.svg")
    this._nsb_elements["nsb_name"].text(node.data.name)

    this._nsb_elements["nsb_description"].val(node.data.description)
    this._description = this._nsb_elements["nsb_description"].val()

    this._original_proficiency_text = this._set_proficiency_text(node);

    this._original_proficiency = this._set_new_progress_length(node);

    // create experiences list
    this._create_experiences(node);

    // close the proficiency menu if is active when updating content.
    if (this._nsb_elements["nsb_proficiency_menu"].attr("data-active") === "true") {
      this._toggle_proficiency_menu()
    }
  }

  /**
   * Shows the sidebar. Slide in animation from right -> left.
   * @param {descendant} d A descendant object from d3.js 
   * @returns 
   */
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

  /**
   * Hides the sidebar. SLide out animation from left -> right.
   * Will ask for confirmation before exit if changes detected.
   * @returns 
   */
  hide() {
    // already hidden
    if (this._nsb.hasClass("translate-x-full")) {
      return;
    }

    if (this.is_editable && !this._toggle_edit()) {
      return;
    }

    this._nsb.addClass("translate-x-full")
    this.is_opened = false;
  }
}
