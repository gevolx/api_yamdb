from rest_framework import serializers

from reviews.models import Comment, Review
from titles.models import SCORE, Category, Genre, Title
from users.models import User

from .utils import generate_confirmation_code, send_verification_mail


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)
        extra_kwargs = {
            'username': {
                "validators": [],
            },
            'email': {
                "validators": [],
            }
        }

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Unavailable username!')
        exists_user = User.objects.filter(
            username=data['username'], email=data['email']
        ).first()
        if exists_user:
            if not exists_user.api_token:
                raise serializers.ValidationError('User already registered!')
            return data
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exist!')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exist!')
        return data

    def create(self, validated_data):
        confirmation_code = generate_confirmation_code()
        email = validated_data['email']
        exists_user = User.objects.filter(
            username=validated_data['username'], email=email
        ).first()
        if not exists_user:
            send_verification_mail(email, confirmation_code)
            return User.objects.create_user(
                **validated_data,
                confirmation_code=confirmation_code
            )
        if not exists_user.api_token:
            exists_user.confirmation_code = confirmation_code
            exists_user.save()
        send_verification_mail(email, confirmation_code)
        return exists_user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='review__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(
        choices=SCORE
    )
    author_id = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'pub_date', 'text', 'score', 'author_id')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        author_id = self.context['request'].user.id

        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв этому произведению.'
            )
        data.update({
            'title_id': title,
            'author_id': author_id
        })
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')
