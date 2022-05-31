(() => {
  // todo: allow multi select of ds to multi delete

  if ($ === undefined) {
    console.error("Manage DS: JQuery not loaded.");
  }

  /**
   * Fills the form with the right data
   * @param {Array<string>} names
   * @param {boolean} submit Auto submit form after filling. Default false.
   */
  function fill_form(names, submit = false) {
    let form_el = $("#delete_ds_form");

    form_el.find("#ddsf_names").val(names.join(","));

    if (submit) form_el.submit();

    form_el = null;
  }

  // enable click three dots to open drop down menu
  $("div[data-menu-button]").click(function (e) {
    const drop_down = $(`#${$(this).attr("data-for-ds")}_drop_down`);
    drop_down.toggleClass("scale-y-0");
  });

  const to_delete_list = [];
  let is_multi_select_on = false;

  // the entire list of desired skills
  const desired_skills_list = $("#desired_skills_list");

  const multi_selection_overlays = desired_skills_list.find(
    "div[select-overlay]"
  );

  const multi_select_toggle = $("#multi_select_toggle");

  multi_select_toggle.click(function () {
    // add as a saving button
    if (is_multi_select_on) {
      if (
        to_delete_list.length > 0 &&
        confirm("Are you sure you want to delete the selected desired skills?")
      ) {
        fill_form(to_delete_list, true);
      }

      // reset overlay status and remove desired skill name from submit list.
      $("div[data-is-selected='true']").click();

      multi_select_toggle.text(multi_select_toggle.attr("data-content"));
    } else {
      multi_select_toggle.text("Save");
    }

    // toggle select-overlay for all desired skills
    multi_selection_overlays.toggleClass("hidden");
    is_multi_select_on = !is_multi_select_on;
  });

  multi_selection_overlays.click(function () {
    const clicked_item = $(this);

    const selection = clicked_item.attr("selection");

    if (clicked_item.attr("data-is-selected") === "true") {
      to_delete_list.splice(to_delete_list.indexOf(selection));
      clicked_item.attr("data-is-selected", "false");
    } else {
      to_delete_list.push(selection);
      clicked_item.attr("data-is-selected", "true");
    }

    clicked_item.toggleClass("!border-red-400");
    clicked_item.find("svg").toggleClass("!text-red-400");
  });

  // these are the menus from clicking the three dots on each desired skill card.
  const drop_down_lists = $("ul[drop-down-list]");
  drop_down_lists.children().click(function (e) {
    const clicked_item = $(this);
    const action = clicked_item.attr("data-action");

    if (action === "delete") {
      fill_form([clicked_item.attr("data-action-content")], true);
    }
  });
})();
