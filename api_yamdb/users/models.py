from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .apps import ROLES, USER, ADMIN, MODERATOR
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, unique=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLES,
        default=USER
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)

    confirmation_code = models.IntegerField(null=True, blank=True)

    api_token = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN
