from rest_framework import serializers

from titles.models import SCORE, Category, Comment, Genre, Title, Review


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

# Нужна модель Review и её атрибут score чтобы запустить этот сериалайзер
# class ReadOnlyTitleSerializer(serializers.ModelSerializer):
#     rating = serializers.IntegerField(
#         source='reviews__score__avg', read_only=True
#     )
#     genre = GenreSerializer(many=True)
#     category = CategorySerializer()
#
#     class Meta:
#         model = Title
#         fields = (
#             'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
#         )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(
        choices=SCORE
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'pub_date', 'text', 'score')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['request']
        author = self.context['request'].user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Ранее вы уже оставляли отзыв данному произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')