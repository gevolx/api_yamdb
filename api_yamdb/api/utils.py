import uuid

from django.core.mail import send_mail
from rest_framework import mixins, viewsets
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


def generate_confirmation_code():
    return uuid.uuid4()


def send_verification_mail(email: str, confirmation_code: int):
    subject = 'YaMDB confirmation code'
    message = (f'Your confirmation code:\n{confirmation_code}\n'
               f'Thanks for using YaMDB.')
    from_email = 'support@yamdb.ru'
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)


def get_token_for_user(user: User):
    token = AccessToken.for_user(user)

    return {
        'token': str(token)
    }


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
