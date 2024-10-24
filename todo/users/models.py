# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    def __str__(self):
        return self.email
