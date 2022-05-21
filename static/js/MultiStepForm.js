function showTab(n) { 
    var tabs = document.getElementsByClassName('tab'); 
    tabs[n].style.display = 'block'; 
    if (n == 0) { 
        document.getElementById("prevBtn").style.diplay = "none";
    } else { 
        document.getElementById('prevBtn').style.display = 'inline';
    }
    fixStepIndicator(n);
}

function nextPrev(n){
    var tabs = document.getElementsByClassName("tab");

    if (n == 1 && !validateForm()) 
        return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;

    if(currentTab >= tab.length){
        document.getElementById("experience-input").submit(); 
        return false;
    }
    showTab(currentTab);
}
function validateForm(){
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");

    for(i = 0; i < y.length; i++){
        if(y[i].value == ""){
            y[i].className += "invalid";
            valid = false;
        }
    }
    if(valid){
        document.getElementsByClassName("step")[currentTab].className
    }
    return valid;
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
      x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}