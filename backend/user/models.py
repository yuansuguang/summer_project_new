from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    user_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class ConfirmCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ": " + self.code
