from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
#from django.utils.decorators import method_decorator #Specific for class views
#from django.views.decorators.cache import cache_page
#from django.views.decorators.vary import vary_on_cookie

from blog.models import Post
from blog.forms import CommentForm

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#@method_decorator(cache_page(300), name="get")
#@method_decorator(vary_on_cookie, name="get")
class PostList(ListView):
    model = Post
    
    def get_queryset(self):
        posts = self.model.objects.filter(published_at__lte=timezone.now())
        logger.debug("Got %d posts", len(posts))
        return posts

class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get(self, request, slug):
        post = get_object_or_404(self.model, slug=slug)
        if request.user.is_active:
            comment_form = CommentForm()
        else:
            logger.info("User is not logged in.")
            comment_form = None
        return render(request, self.template_name, {"post": post, "comment_form": comment_form})
    
    def post(self, request, slug):
        post = get_object_or_404(self.model, slug=slug)
        if request.user.is_active:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)

            logger.debug("Form for comment is not valid.")
        else:
            logger.info("A POST request was sent without the user logged in!")
            comment_form = None
        return render(request, self.template_name, {"post": post, "comment_form": comment_form})
