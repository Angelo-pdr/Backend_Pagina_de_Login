from django.urls import include, path
from rest_framework import routers
from core.views import UserViewSet, GroupViewSet
from django.contrib import admin

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
admin


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
