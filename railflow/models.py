from django.db import models
import random

# Create your models here.

class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name

class CargoType(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Train(models.Model):
    number = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.number} - {self.brand}"


class Alert(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class AlertCard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


""" class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origin} to {self.destination}" """


class ReasonInspection(models.Model):
    description = models.CharField(25)

    def __str__(self):
        return self.description


class Inspection(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    reason = models.ForeignKey(ReasonInspection, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inspection of {self.train.number} on {self.date}"


class reasonMaintenance(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Maintenance(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    reason = models.ForeignKey(reasonMaintenance, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Maintenance of {self.train.number} on {self.date}"


class Company(models.Model):
    name = models.CharField(max_length=50, null=False)
    cnpj = models.CharField(max_length=18, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_ref = random.randint(00000, 99999)
        if not Order.objects.filter(order_number=unique_ref).exists():
            not_unique = False
    return str(unique_ref)
    
class Order(models.Model):
    order_number = models.CharField(
        max_length=5, null=False, unique=True, default=create_new_ref_number)
    cargo_type = models.ForeignKey(CargoType, on_delete=models.CASCADE)
    weight = models.FloatField()
    origin = models.ForeignKey(Station, related_name='origin_orders', on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name='destination_orders', on_delete=models.CASCADE)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.order_number} from {self.origin} to {self.destination}"

    
