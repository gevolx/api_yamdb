from rest_framework import serializers

from .helpers import generate_confirmation_code, send_verification_mail
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        confirmation_code = generate_confirmation_code()
        user = User.objects.create_user(**validated_data,
                                        confirmation_code=confirmation_code)
        send_verification_mail(validated_data['email'], confirmation_code)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
