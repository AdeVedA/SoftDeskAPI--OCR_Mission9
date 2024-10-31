# users/models.py
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email,and password.
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('L\'Email doit être renseigné')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise e

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        if 'age' not in extra_fields:
            raise ValueError('L\'âge doit être renseigné')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
An abstract base class implementing a fully featured User model with
admin-compliant permissions.
"""

    username = models.CharField(max_length=30, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(120)])
    email = models.EmailField(max_length=40, unique=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
