from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль',
        blank=True,
        max_length=50
    )
