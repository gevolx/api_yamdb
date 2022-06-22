from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignUpView, GetTokenView, UsersViewSet,
    CategoryViewSet, GenreViewSet, ReviewViewSet,
    CommentViewSet  # , TitleViewSet
)

app_name = 'api'

api_router = DefaultRouter()

api_router.register(r'users', UsersViewSet)
api_router.register(r'categories', CategoryViewSet)
api_router.register(r'genres', GenreViewSet)
# api_router.register(r'titles', TitleViewSet)
api_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet
)
api_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet
)

urlpatterns = [
    path('v1/', include(api_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
]
