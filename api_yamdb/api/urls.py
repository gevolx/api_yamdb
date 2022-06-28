from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CurrentUserView,
                    GenreViewSet, GetTokenView, ReviewViewSet, SignUpView,
                    TitleViewSet, UsersViewSet)

app_name = 'api'

api_router = DefaultRouter()

api_router.register(r'users', UsersViewSet)
api_router.register(r'categories', CategoryViewSet)
api_router.register(r'genres', GenreViewSet)
api_router.register(r'titles', TitleViewSet)
api_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet, basename='Review'
)
api_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='Comment'
)

auth_urls = [
    path('signup/', SignUpView.as_view()),
    path('token/', GetTokenView.as_view()),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/users/me/', CurrentUserView.as_view()),
    path('v1/', include(api_router.urls)),
]
