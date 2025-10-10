from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from railflow.views import CargoTypeViewSet, TrainViewSet, AlertViewSet, AlertCardViewSet, reasonMaintenanceViewSet, MaintenanceViewSet, ReasonInspectionViewSet, InspectionViewSet, CompanyViewSet, OrderViewSet, StationViewSet

router = DefaultRouter()
router.register(r"cargotypes", CargoTypeViewSet)
router.register(r"trains", TrainViewSet)
router.register(r"alerts", AlertViewSet)
router.register(r"alertcards", AlertCardViewSet)
router.register(r"reasoninspections", ReasonInspectionViewSet)
router.register(r"inspections", InspectionViewSet)
router.register(r"reasonmaintenances", reasonMaintenanceViewSet)
router.register(r"maintenances", MaintenanceViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"stations", StationViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path('api/', include('railflow.urls')),
]
