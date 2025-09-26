from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from railflow.models import CargoType, Alert, Train, AlertCard

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
    
    class Meta:
        model = AlertCard
        fields = ['id', 'title', 'content', 'created_at', 'train', 'train_number', 'alert']