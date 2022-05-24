(() => {
    const search_form = $("#search_form")
  
    if (search_form.lenght < 1) {
      console.error("Could not find search form.")
      return;
    }
    
    const search_endpoint = search_form.attr("action")
    /**
     * @type {string}
     */
    const method = search_form.attr("method")
    const static_url = search_form.attr('data-static-url')
    
    const search_bar = $("#search_bar");
    const search_query = $("#search_query")
    const search_scope = $("#search_scope")
    const search_icon = $("#search_icon")
    const search_result_list = $("#search_result_list")
    const search_result_item = $("#search_result_item") // result item template
    const search_scope_list = $("#search_scope_list")
    const search_scope_items = search_scope_list.children()
    const search_result_container = $("#search_result_container")
    const search_scope_menu = $("#search_scope_menu")
    const current_scope_text = $("#current_scope_text")
    const search_scope_filter = $("#search_scope_filter")
    const filter_arrow = $("#filter_arrow")
    
    function exp_getter(exp_id) {
        if (exp_id.val() === "") {
        console.log("No ID provided")
        }

        fetch(`${search_endpoint}?${new URLSearchParams({
        "csrfmiddlewaretoken": formData.get("csrfmiddlewaretoken"),
        "exp_id": exp_id,
        })}`, {
        method: method.toUpperCase()
        })
        .then(res => res.json())
        .then(data => {
            populateAndShowModal(data)
        })
        .catch(console.error);
    }


    // 
    function populateAndShowModal(data) { 
        
    }
})