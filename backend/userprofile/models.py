from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='userprofile/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class ConfirmEmailUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()
