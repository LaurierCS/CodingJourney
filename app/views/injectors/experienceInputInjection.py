from app.forms import ExperienceInputform

def experience_input_injection(request, context, form=None):
    if form: 
        context['experience_input_form'] = form
    else: 
        user = request.user.profile
        form = ExperienceInputform(user_id=user)
        context['experience_input_form'] = form
    return form