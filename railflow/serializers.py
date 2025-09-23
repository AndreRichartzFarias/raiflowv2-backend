from rest_framework.serializers import ModelSerializer

from railflow.models import CargoType, Alert, Train

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
