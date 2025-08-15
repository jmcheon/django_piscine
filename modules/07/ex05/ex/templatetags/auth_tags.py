from django import template
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()


@register.inclusion_tag("ex/partials/login_form.html")
def login_form():
    # This function provides the AuthenticationForm to its template.
    return {"login_form": AuthenticationForm()}


@register.filter(name="truncate_chars")
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value
