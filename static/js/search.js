(() => {
  const search_form = $("#search_form")

  if (search_form.length < 1) {
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

  // current filtering strategy
  let current_scope = search_scope_filter.attr("data-current-scope")


  function toggleFilterMenu() {
    search_scope_menu.toggleClass("scale-y-0")
    filter_arrow.toggleClass("rotate-180")
  }

  // toggle filter menu
  search_scope_filter.click(toggleFilterMenu);
  
  // listen to selection of a scope
  search_scope_items.click((e) => {
    let new_scope = e.target.getAttribute("data-scope")
    if (current_scope === new_scope) return;

    current_scope = new_scope;
    current_scope_text.text(current_scope);
    search_scope_filter.attr("data-current-scope", current_scope);
    search_scope.val(current_scope)
    
    // focus on search input
    search_query.focus()
  
    // do quick query
    quick_query();
  });

  /**
   * Does a GET request and displays the results in a minimized version, like how google shows possible results.
   */
  function quick_query() {
    if (search_query.val() === "") {
      showSearchResults({results: []})
      return;
    }
    
    // animate search bar
    search_bar.toggleClass("animate-pulse")

    const formData = new FormData(search_form[0])
    fetch(`${search_endpoint}?${new URLSearchParams({
      "csrfmiddlewaretoken": formData.get("csrfmiddlewaretoken"),
      "search_query": formData.get("search_query"),
      "search_scope": formData.get("search_scope"),
      "quick_query": "true"
    })}`, {
      method: method.toUpperCase()
    })
      .then(res => res.json())
      .then(data => {
        search_bar.toggleClass("animate-pulse")
        showSearchResults(data)
      })
      .catch(console.error);
  }

  function showSearchResults(query_data) {
    // clear all previous results
    search_result_list.children().remove("[data-removable-result=\"true\"]");

    console.log(query_data)

    // construct the result lists
    for (let i=0;i<query_data.entries;i++) {
      let result = query_data.results[i]
      let result_item = search_result_item.clone()
      result_item.find("#search_result_link")
      result_item.attr("id", `search_result_link_${result.text}`)
      result_item.attr("data-removable-result", "true")
      result_item.attr("aria-hidden", "false")
      result_item.removeClass("hidden")
      result_item.find("#search_result_link").attr("href", result.url)
      result_item.find("#search_result_text").text(result.text)
      result_item.find("#search_result_category").text(result.category)
      
      if (result.category === "user") {
        result_item.find("#search_result_image").attr("src", `${static_url}${result.image}`)
        result_item.find("#search_result_image").removeClass("hidden")
      }
      
      search_result_list.append(result_item);
    }

    if (search_result_list.children().length > 1) {
      search_result_container.removeClass("hidden")
    } else {
      search_result_container.addClass("hidden")
    }
  }

  // only show quick query results when search bar is focused.
  search_query.focus(() => {
    search_result_container.removeClass("opacity-60");
  });

  search_query.blur(() => {
    search_result_container.addClass("opacity-60");
  })

  // debounce function is from debounce.js
  search_query.keyup(debounce(quick_query))
})();