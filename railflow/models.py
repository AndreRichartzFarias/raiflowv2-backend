from django.db import models

# Create your models here.


class CargoType(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Train (models.Model):
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
