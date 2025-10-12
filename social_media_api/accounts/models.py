from django.contrib.auth.models import AbstractUser
from django.db import models


def profile_image_upload_to(instance, filename):
    return f'profiles/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_image_upload_to, null=True, blank=True)
    # users this user follows
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username