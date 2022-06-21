from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль',
        blank=True,
        max_length=50
    )

    confirmation_code = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(_('active'), default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
