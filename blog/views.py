from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView

from blog.models import Post
from blog.forms import CommentForm

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(published_at__lte=timezone.now())

class PostDetail(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get(self, request, slug):
        post = get_object_or_404(self.model, slug=slug)
        if request.user.is_active:
            comment_form = CommentForm()
        else:
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
                return redirect(request.path_info)
        else:
            comment_form = None
        return render(request, self.template_name, {"post": post, "comment_form": comment_form})
