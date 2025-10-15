from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
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
    return JsonResponse({"message": "CSRF cookie set"})

@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        email = data["email"]
        password = data["password"]
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

    # Use email for authentication (requires custom backend)
    user = authenticate(request, email=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({"success": True})
    return JsonResponse(
        {"success": False, "message": "Invalid credentials"}, status=401
    )

def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})
@login_required
@require_http_methods(["GET"])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )
    return JsonResponse({"message": "Not logged in"}, status=401)

@login_required
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
    permission_classes = [IsAuthenticated]


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [IsAuthenticated]


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

class AlertCardViewSet(ModelViewSet):
    queryset = AlertCard.objects.all()
    serializer_class = AlertCardSerializer
    permission_classes = [IsAuthenticated]

class ReasonInspectionViewSet(ModelViewSet):
    queryset = ReasonInspection.objects.all()
    serializer_class = ReasonInspectionSerializer
    permission_classes = [IsAuthenticated]

class InspectionViewSet(ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [IsAuthenticated]

class reasonMaintenanceViewSet(ModelViewSet):
    queryset = reasonMaintenance.objects.all()
    serializer_class = reasonMaintenanceSerializer
    permission_classes = [IsAuthenticated]

class MaintenanceViewSet(ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]