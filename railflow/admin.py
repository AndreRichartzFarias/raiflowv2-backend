from django.contrib import admin

# Register your models here.


from .models import CargoType

admin.site.register(CargoType)