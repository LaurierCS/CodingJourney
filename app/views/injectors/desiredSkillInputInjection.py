from app.forms import DesiredSkillsInputForm

def desired_skill_input_injection(request, context, form=None):
    if form: 
        context['desired_skill_form'] = form
    else: 
        user = request.user.profile
        form = DesiredSkillsInputForm(user)
        context['desired_skill_form'] = form

# needs to be edited slightly for update
    if request.GET.get("id"):
        context["action"] = "update"
    return form