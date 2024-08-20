from django.db import models
from django.contrib.auth.models import User


def avatar_directory_path(instance: "User", filename: str) -> str:
    return "users/user_{pk}/avatar_image/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)

