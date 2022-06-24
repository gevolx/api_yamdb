from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import (PageNumberPagination)

from users.apps import USER
from users.models import User
from titles.models import Category, Genre, Title, Review
from .filters import TitlesFilter
from .helpers import get_token_for_user
from .serializers import (
    SignUpSerializer, TokenSerializer, UsersSerializer,
    CategorySerializer, GenreSerializer, CommentSerializer,
    TitleSerializer, ReviewSerializer, ReadOnlyTitleSerializer
)
from .permissions import IsAdminOrReadOnly, AuthorOrReadonly, IsAdministrator
from .utils import ListCreateDestroyViewSet


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if user.confirmation_code != confirmation_code:
                return Response({'Error': f'Confirmation code is not valid!'},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.api_token:
                user.api_token = True
                user.save()
            return Response(get_token_for_user(user), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = (IsAdministrator,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination


class CurrentUserView(APIView):

    def get(self, request):
        serializer = UsersSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user_obj = User.objects.get(id=self.request.user.id)
        serializer = UsersSerializer(user_obj, data=self.request.data, partial=True)
        if serializer.is_valid():
            if user_obj.is_user:
                serializer.validated_data['role'] = USER
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("review__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrReadonly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.review.all()
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrReadonly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=title
        )
        return review.comment.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=title
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
