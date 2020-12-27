from django.contrib import admin

from .models import DocumentPost, Comment, Like, Dislike


admin.site.register(DocumentPost)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)
