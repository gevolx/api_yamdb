<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, GetTokenView, UsersViewSet

app_name = 'api'

api_router = DefaultRouter()

api_router.register(r'users', UsersViewSet)

urlpatterns = [
    path('v1/', include(api_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
]
=======
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet#, TitleViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
# router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
>>>>>>> develop
