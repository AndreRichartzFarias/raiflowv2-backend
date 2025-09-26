from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from railflow.views import CargoTypeViewSet, TrainViewSet, AlertViewSet, AlertCardViewSet

router = DefaultRouter()
router.register(r"cargotypes", CargoTypeViewSet)
router.register(r"trains", TrainViewSet)
router.register(r"alerts", AlertViewSet)
router.register(r"alertcards", AlertCardViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path('api/', include('railflow.urls')),
]
