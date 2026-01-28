from django.contrib import admin

from blog.models import Tag, Post, Comment

class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}
  #exclude = ("slug",)
  list_display = ("slug", "published_at")

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
