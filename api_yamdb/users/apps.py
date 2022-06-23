from django.apps import AppConfig

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLES = [
    (ADMIN, 'Administrator'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
]


class UsersConfig(AppConfig):
    name = 'users'
