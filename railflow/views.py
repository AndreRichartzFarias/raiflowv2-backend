from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from railflow.models import CargoType, Train, Alert
from railflow.serializers import CargoTypeSerializer, TrainSerializer, AlertSerializer


class CargoTypeViewSet(ModelViewSet):
    queryset = CargoType.objects.all()
    serializer_class = CargoTypeSerializer

class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
