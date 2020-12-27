from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class DocumentPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def approve_likes(self):
        return self.likes.filter(approved_like=True)

    def approve_dislikes(self):
        return self.dislikes.filter(approved_like=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('files.DocumentPost', related_name='comments', on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Like(models.Model):
    post = models.ForeignKey('files.DocumentPost', related_name='liked_post', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', related_name='liker', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)

class Dislike(models.Model):
    post = models.ForeignKey('files.DocumentPost', related_name='disliked_post', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', related_name='disliker', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)
