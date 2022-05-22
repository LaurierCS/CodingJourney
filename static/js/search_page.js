(() => {

  // assert for jquery
  if ($ === undefined) {
    console.error("JQuery not loaded.")
    return;
  }

  // find all elements
  const filter_list = $("#filter_list")
  const result_list = $("#search_result_olist")

  let active_filter = filter_list.find('li[active]')
  let filter_strategy = active_filter.attr('data-filter')

  active_filter.addClass("bg-primary")
  active_filter.removeClass("hover:bg-primary-darker")
  
  filter_list.children().click(function () {
    const clicked_item = $(this)
    
    // if the same filter is clicked, do nothing
    if (active_filter.attr('data-filter') === clicked_item.attr('data-filter')) return;
    
    // update styling
    clicked_item.removeClass("hover:bg-primary-darker")
    clicked_item.addClass("bg-primary")

    active_filter.addClass("hover:bg-primary-darker")
    active_filter.removeClass("bg-primary")

    filter_strategy = clicked_item.attr('data-filter')

    active_filter = clicked_item;

    // show/hide new list of results
    toggleResults()
  })

  function toggleResults() {
    // hide all elements
    result_list.children().fadeOut(250)
      .promise()
      .done(function () {

        if (filter_strategy === 'all') {
          result_list.children().fadeIn(250);
          return;
        }
        
        result_list.find(`li[data-category="${filter_strategy}"]`).fadeIn(250);

        if (filter_strategy === 'skill') {
          result_list.find('li[data-category="skill category"]').fadeIn(250);
        }
      });
  }

})();