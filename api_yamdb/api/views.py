from rest_framework import status, viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .helpers import get_token_for_user
from .serializers import (
    SignUpSerializer, TokenSerializer, UsersSerializer,
    CategorySerializer, GenreSerializer,
    # ReadOnlyTitleSerializer,
)

from titles.models import Category, Genre
from .permissions import IsAdminOrReadOnly
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
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response(get_token_for_user(user), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = self.request.user.pk
        return super(UsersViewSet, self).get_object()


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

# Нужна модель Review и её атрибут score чтобы запустить этот эндпоинт
# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all().annotate(
#         Avg("reviews__score")
#     ).order_by("name")
#     serializer_class = TitleSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = TitlesFilter
#
#     def get_serializer_class(self):
#         if self.action in ("retrieve", "list"):
#             return ReadOnlyTitleSerializer
#         return TitleSerializer
