(() => {

  if ($ === undefined) {
    console.error("JQuery is not loaded.")
    return;
  }


  const menu_list = $("#sidemenu").find("ul").children();

  menu_list.each(function () {
    const current = $(this);

    const is_expandable = current.attr("data-expandable-menu") === "true"
    const allow_expand = current.attr("data-expandable-at") === window.location.pathname;

    if (is_expandable && allow_expand) {
      const submenu = $(current.attr("data-expand-target"));
      submenu.removeClass("hidden");
    }
  });

})();