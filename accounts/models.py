from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    address = models.TextField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    picture_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    picture_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")

    def __unicode__(self):
        return self.user.username