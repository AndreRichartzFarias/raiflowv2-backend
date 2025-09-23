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