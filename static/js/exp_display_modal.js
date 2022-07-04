    
/**
 * @type {string}
 */
function exp_getter(exp_id, modal_id) {
    let origin = window.location.origin
    let search_endpoint = origin + "/experience-view-handler"
    fetch(`${search_endpoint}?${new URLSearchParams({
    // "csrfmiddlewaretoken": formData.get("csrfmiddlewaretoken"),
    "exp_id": exp_id, //request.GET.get("exp_id")
    })}`, {
    method: "GET"
    })
    .then(res => res.json())
    .then(data => {
        populateAndShowModal(data, modal_id)
    })
    .catch(console.error);
}


function populateAndShowModal(data, modal_id) { 
    exp = data["experience"];
    // set title
    $("#experience-name").text(exp["name"]);
    // set likes
    $("#likes-icon").text(exp["likes"] + " Likes");
    // set description
    $("#modal-description").text(exp["description"]);
    // set skills
    const skills_colors = ["tech-tag-blue", "tech-tag-green", "tech-tag-orange"];
    let skills_html = "";
    let selector = 0;
    for (let skill of exp["skills"]) { 
        skills_html += `<div class="tech-tag ${skills_colors[selector]} p-2 ml-0">${skill["skill_name"]}</div> \n`;
        selector = (selector + 1)%skills_colors.length;
    }
    $("#tech-tag-container").html(skills_html);
    // set start date
    $("#modal-start-date").text(exp["start_date"]);
    // set end date
    $("#modal-end-date").text(exp["end_date"]);
    // set project link
    $("#modal-project-link").html(exp["url"]);

    // console.log(data)
    modalOpenBehaviour(modal_id)
    // console.log(project_name);
} 