from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, DiskUrlViewSet

router = DefaultRouter()
router.register(r"file",  FileViewSet)
router.register(
    r"url-disk",
    DiskUrlViewSet,
    basename="url-disk",
)

urlpatterns = [
    path("api/", include(router.urls)),
]
