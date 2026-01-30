from django.contrib.auth.models import User
from django.template import Library
from django.utils.html import format_html

from blog.models import Post

import logging

logger = logging.getLogger(__name__)
register = Library()

#@register.inclusion_tag("blog/title_post_list.html", takes_context=True)
#def recent_posts(context):
@register.inclusion_tag("blog/title_post_list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
    return {"title": "Recent Posts", "post_list": posts}

#@register.simple_tag(takes_context=True)
#def author_details_tag(context):
    #current_user = context["user"]
    #user = context["post"].author
@register.filter
def author_details(user, current_user):
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

@register.simple_tag()
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")