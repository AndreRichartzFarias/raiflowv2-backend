from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

from railflow.models import CargoType, Train, Alert, AlertCard, reasonMaintenance, Maintenance, ReasonInspection, Inspection, Company, Order, Station
from railflow.serializers import CargoTypeSerializer, TrainSerializer, AlertSerializer, AlertCardSerializer, reasonMaintenanceSerializer, MaintenanceSerializer, ReasonInspectionSerializer, InspectionSerializer, CompanySerializer, OrderSerializer, StationSerializer

def api_root(request):
    return JsonResponse({"message": "Bem-vindo à API Raiflow!"})
@ensure_csrf_cookie
@require_http_methods(["GET"])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({"message": "CSRF cookie set"})


@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        email = data["email"]
        password = data["password"]
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({"success": True})
    return JsonResponse(
        {"success": False, "message": "Invalid credentials"}, status=401
    )


def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@require_http_methods(["GET"])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {"username": request.user.username, "email": request.user.email}
        )
    return JsonResponse({"message": "Not logged in"}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    data = json.loads(request.body.decode("utf-8"))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": "User registered successfully"}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({"error": errors}, status=400)


class CargoTypeViewSet(ModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

class AlertCardViewSet(ModelViewSet):
    queryset = AlertCard.objects.all()
    serializer_class = AlertCardSerializer

class ReasonInspectionViewSet(ModelViewSet):
    queryset = ReasonInspection.objects.all()
    serializer_class = ReasonInspectionSerializer

class InspectionViewSet(ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

class reasonMaintenanceViewSet(ModelViewSet):
    queryset = reasonMaintenance.objects.all()
    serializer_class = reasonMaintenanceSerializer

class MaintenanceViewSet(ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer