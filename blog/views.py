from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.views.generic import ListView, DetailView

# Create your views here.

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(published_at__lte=timezone.now())

class PostDetail(DetailView):
    model = Post
