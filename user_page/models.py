from django.conf import settings
from django.urls import reverse
from django.db import models
from PIL import Image

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    phone_no = models.CharField(max_length = 20,default='')
    first_name = models.CharField(max_length = 20,default='')
    last_name = models.CharField(max_length = 20,default='')
    image = models.ImageField(upload_to='profile_pics')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "first_name"]


class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.DO_NOTHING)
    following = models.ForeignKey(User, related_name='following', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)
