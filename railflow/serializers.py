from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

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

class AlertCardSerializer(ModelSerializer):
    train_number = serializers.CharField(source='train.number', read_only=True)
    alert = AlertSerializer()
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
    origin = serializers.CharField(source='origin.name', read_only=True)
    destination = serializers.CharField(source='destination.name', read_only=True)
    cargo_type_description = serializers.CharField(source='cargo_type.description', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'cargo_type', 'cargo_type_description', 'weight', 'origin', 'destination', 'departure_date', 'arrival_date', 'company', 'company_name']

class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'