function showDescription(project_id)
    console.log("clicked project: " + project_id)
    desc = document.querySelector(`#proj-desc-${project_id}`)
    
    if (desc.classList.contains("hidden")) { 
        desc.className.replace
      ( /(?:^|\s)hidden(?!\S)/g , '' )
    } else { 
        desc.className += " hidden"
    }

showDescription(1)