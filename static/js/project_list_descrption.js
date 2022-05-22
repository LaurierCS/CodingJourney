let prev_desc = undefined;
function showDescription(project_id) {
    desc = document.querySelector(`#proj-desc-${project_id}`);
    
    if (desc.classList.contains("hidden")) { 
        desc.classList.remove('hidden');
        setTimeout(function() { 
            desc.classList.remove('opacity-0')
        }, 20);
    } else { 
        desc.classList.add('opacity-0'); 
        desc.addEventListener('transitionend', function(e) { 
            desc.classList.add('hidden');
        }, {
            capture: false, 
            once: true, 
            passive: false
        })
    }
}

// showDescription(1)