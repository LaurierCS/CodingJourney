function modalOpenBehaviour(modalId) { 
    let modal = document.getElementById(modalId);
    console.log(modal);
    modal.style.display = "flex";
}

function modalCloseBehaviour(modalId) { 
    let modal = document.getElementById(modalId);

    modal.style.display = "none"
}

var currentTab = 0;
showTab(currentTab); 

function translateLeftByWidth(className, maxTabs) {
    let elems = document.getElementsByClassName(className);
    let width = elems[0].clientWidth
    
    if (currentTab < maxTabs) {
        currentTab = currentTab + 1;
        for (let elem of elems) {
            elem.style.transform = "translateX(" + -width*currentTab + "px)"
        }
    }
    
}

function translateRightByWidth(className) {
    let elems = document.getElementsByClassName(className);
    let width = elems[0].clientWidth
    
    if (currentTab > 0) {
        currentTab = currentTab - 1;
        for (let elem of elems) {
            elem.style.transform = "translateX(" + -width*currentTab + "px)"
        }
    }

}