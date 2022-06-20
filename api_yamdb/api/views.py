from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from titles.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)
                         # ReadOnlyTitleSerializer,)
from .utils import ListCreateDestroyViewSet
from .filters import TitlesFilter


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
