function modalOpenBehaviour(modalId) { 
    let modal = document.getElementById(modalId);
    console.log(modal);
    modal.style.display = "flex";
}

function modalCloseBehaviour(modalId) { 
    let modal = document.getElementById(modalId);

    modal.style.display = "none"
}
