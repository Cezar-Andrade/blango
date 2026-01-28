from django.contrib.auth.models import User
from django.template import Library
from django.utils.html import format_html

register = Library()

@register.filter
def author_details(user, current_user=None):
    if not isinstance(user, User):
        return ""

    if user.first_name and user.last_name:
        name = f"{user.first_name} {user.last_name}"
    else:
        name = user.username

    if user == current_user:
        name = format_html("<strong>{}</strong>", name)
    elif user.email:
        name = format_html("<a href='mailto:{}'>{}</a>", user.email, name)

    return name