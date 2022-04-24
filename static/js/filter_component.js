(() => {
  // handling styling when opening
  const drop_down = document.getElementById("drop_down");
  const filter = document.getElementById("filter");
  drop_down.is_hidden = drop_down.classList.contains("hidden");
  filter.addEventListener('click', (_e) => {
    if (drop_down.is_hidden) {
      drop_down.is_hidden = false;
      drop_down.dataset["active"] = "true"
      filter.dataset["active"] = "true"
    } else {
      drop_down.is_hidden = true;
      filter.dataset["active"] = "false"
      drop_down.dataset["active"] = "false"
    }
  });

  // handling filter selection listeners
  const selections = document.getElementById("list");
  const query_text = document.getElementById("query_text");
  const submit = document.getElementById("submit");
  // adding click event listener to all filtering selections, not great, but it works fine because there are not a lot of them
  for (let i=0;i<selections.children.length;i++) { 
    selections.children.item(i).addEventListener('click', (e) => {
      query_text.value = e.target.dataset["value"];
      submit.click(); // submit the form affect selecting a filter
    });
  }
})();