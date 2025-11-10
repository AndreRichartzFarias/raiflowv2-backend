from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db import transaction
from .models import Estacao, Rota, RotaEstacao
import math

from railflow.models import CargoType, Alert, Train, AlertCard, reasonMaintenance, Maintenance, ReasonInspection, Inspection, Company, Order, Station

class CargoTypeSerializer(ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class TrainSerializer(ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class AlertSerializer(ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class AlertCardSerializer(serializers.ModelSerializer):
    train_number = serializers.CharField(source='train.number', read_only=True)
    alert = AlertSerializer(read_only=True)          
    class Meta:
        model = AlertCard
        fields = ['id', 'title', 'content', 'created_at', 'train', 'train_number', 'alert']

class ReasonInspectionSerializer(ModelSerializer):
    class Meta:
        model = ReasonInspection
        fields = '__all__'

class InspectionSerializer(ModelSerializer):
    train_number = serializers.CharField(source='train.number', read_only=True)
    reason_description = serializers.CharField(source='reason.description', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'train', 'train_number', 'reason', 'reason_description', 'date', 'notes']

class reasonMaintenanceSerializer(ModelSerializer):
    class Meta:
        model = reasonMaintenance
        fields = '__all__'

class MaintenanceSerializer(ModelSerializer):
    train_number = serializers.CharField(source='train.number', read_only=True)
    reason_description = serializers.CharField(source='reason.description', read_only=True)

    class Meta:
        model = Maintenance
        fields = ['id', 'train', 'train_number', 'reason', 'reason_description', 'date', 'notes']

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    cargo_type_description = serializers.CharField(source='cargo_type.description', read_only=True)
    origin = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    destination = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    origin_name = serializers.CharField(source='origin.name', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number',
            'cargo_type', 'cargo_type_description',
            'weight',
            'origin', 'origin_name',
            'destination', 'destination_name',
            'departure_date', 'arrival_date',
            'company', 'company_name'
        ]
        read_only_fields = ['order_number']
        
class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class EstacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacao
        fields = ['id', 'nome', 'latitude', 'longitude', 'endereco', 'data_criacao']


class RotaEstacaoSerializer(serializers.ModelSerializer):
    estacao = EstacaoSerializer(read_only=True)
    estacao_id = serializers.PrimaryKeyRelatedField(
        source='estacao', queryset=Estacao.objects.all(), write_only=True
    )

    class Meta:
        model = RotaEstacao
        fields = ['id', 'ordem', 'estacao', 'estacao_id']


class RotaSerializer(serializers.ModelSerializer):
    estacoes = serializers.SerializerMethodField(read_only=True)
    estacoes_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Rota
        fields = [
            'id', 'nome', 'distancia_km', 'tempo_estimado_min',
            'data_criacao', 'estacoes', 'estacoes_ids'
        ]
        read_only_fields = ['distancia_km', 'tempo_estimado_min', 'data_criacao', 'estacoes']

    def get_estacoes(self, obj):
        rels = obj.rota_estacoes.select_related('estacao').order_by('ordem')
        return EstacaoSerializer([r.estacao for r in rels], many=True).data

    @staticmethod
    def haversine_km(lat1, lon1, lat2, lon2):
       
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def compute_distance_and_time(self, station_ids):
        if not station_ids:
            return 0.0, 0


        try:
            ids = [int(x) for x in station_ids]
        except Exception:
            return 0.0, 0

        stations_dict = Estacao.objects.in_bulk(ids)

        ordered = [stations_dict.get(i) for i in ids if stations_dict.get(i) is not None]

        if len(ordered) < 2:
            return 0.0, 0

        total_km = 0.0
        for s1, s2 in zip(ordered, ordered[1:]):
            if not s1 or not s2:
                continue
            try:
                lat1 = float(s1.latitude)
                lon1 = float(s1.longitude)
                lat2 = float(s2.latitude)
                lon2 = float(s2.longitude)
            except Exception:
                continue
            total_km += self.haversine_km(lat1, lon1, lat2, lon2)

        distancia = round(total_km, 2)
        
        tempo_min = int(round(distancia)) if distancia > 0 else 0
        return distancia, tempo_min

    def create(self, validated_data):
        station_ids = validated_data.pop('estacoes_ids', [])
        with transaction.atomic():
            distancia, tempo_min = self.compute_distance_and_time(station_ids) if station_ids else (None, None)
            rota = Rota.objects.create(distancia_km=distancia, tempo_estimado_min=tempo_min, **validated_data)
            if station_ids:
                bulk = []
                for idx, sid in enumerate(station_ids):
                    bulk.append(RotaEstacao(rota=rota, estacao_id=sid, ordem=idx))
                RotaEstacao.objects.bulk_create(bulk)
        return rota

    def update(self, instance, validated_data):
        station_ids = validated_data.pop('estacoes_ids', None)
        with transaction.atomic():
            for attr, val in validated_data.items():
                setattr(instance, attr, val)
            if station_ids is not None:
               
                instance.rota_estacoes.all().delete()
                distancia, tempo_min = self.compute_distance_and_time(station_ids) if station_ids else (None, None)
                instance.distancia_km = distancia
                instance.tempo_estimado_min = tempo_min
                bulk = []
                for idx, sid in enumerate(station_ids):
                    bulk.append(RotaEstacao(rota=instance, estacao_id=sid, ordem=idx))
                RotaEstacao.objects.bulk_create(bulk)
            else:
            
                pass
            instance.save()
        return instance