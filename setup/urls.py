from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from core.views import UserViewSet, GroupViewSet, register, CustomAuthToken
from django.contrib import admin

from setup.settings import STATIC_URL

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/register/', register, name='register'),
]
