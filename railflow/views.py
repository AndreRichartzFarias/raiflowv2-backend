from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Q
from accounts.permissions import GroupRequiredPermission

from railflow.models import CargoType, Train, Alert, AlertCard, reasonMaintenance, Maintenance, ReasonInspection, Inspection, Company, Order, Station, Estacao, Rota, RotaEstacao
from railflow.serializers import CargoTypeSerializer, TrainSerializer, AlertSerializer, AlertCardSerializer, reasonMaintenanceSerializer, MaintenanceSerializer, ReasonInspectionSerializer, InspectionSerializer, CompanySerializer, OrderSerializer, StationSerializer, EstacaoSerializer, RotaSerializer, RotaEstacaoSerializer

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
    permission_classes = [DjangoModelPermissions]


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [DjangoModelPermissions]


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [DjangoModelPermissions]

class AlertCardViewSet(ModelViewSet):
    queryset = AlertCard.objects.all()
    serializer_class = AlertCardSerializer
    permission_classes = [DjangoModelPermissions]

class ReasonInspectionViewSet(ModelViewSet):
    queryset = ReasonInspection.objects.all()
    serializer_class = ReasonInspectionSerializer
    permission_classes = [DjangoModelPermissions]

class InspectionViewSet(ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [DjangoModelPermissions]

class reasonMaintenanceViewSet(ModelViewSet):
    queryset = reasonMaintenance.objects.all()
    serializer_class = reasonMaintenanceSerializer
    permission_classes = [DjangoModelPermissions]

class MaintenanceViewSet(ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [DjangoModelPermissions]

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [DjangoModelPermissions]

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [DjangoModelPermissions]

class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [DjangoModelPermissions]

class EstacaoViewSet(ModelViewSet):
    queryset = Estacao.objects.all()
    serializer_class = EstacaoSerializer
    permission_classes = [DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = Estacao.objects.all()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset.order_by('nome')

class RotaEstacaoViewSet(ModelViewSet):
    queryset = RotaEstacao.objects.select_related('rota', 'estacao').all()
    serializer_class = RotaEstacaoSerializer
    permission_classes = [DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = RotaEstacao.objects.select_related('rota', 'estacao')
        rota_id = self.request.query_params.get('rota')
        if rota_id:
            queryset = queryset.filter(rota_id=rota_id)
        return queryset.order_by('rota', 'ordem')

class RotaViewSet(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [DjangoModelPermissions, GroupRequiredPermission]
    required_groups = []
    
    def get_queryset(self):
        queryset = Rota.objects.prefetch_related(
            Prefetch(
                'rota_estacoes',
                queryset=RotaEstacao.objects.select_related('estacao').order_by('ordem')
            )
        )
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset.order_by('nome')
    
    @action(detail=True, methods=['get'])
    def estacoes(self, request, pk=None):
        """Get all stations for a specific route"""
        rota = self.get_object()
        estacoes_rels = rota.rota_estacoes.select_related('estacao').order_by('ordem')
        estacoes = [rel.estacao for rel in estacoes_rels]
        serializer = EstacaoSerializer(estacoes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search routes by name or station name"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        queryset = self.get_queryset().filter(
            Q(nome__icontains=query) |
            Q(rota_estacoes__estacao__nome__icontains=query)
        ).distinct()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)