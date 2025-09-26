from django.contrib import admin

# Register your models here.


from .models import CargoType
from .models import Train
from .models import Alert
from .models import AlertCard

admin.site.register(CargoType)
admin.site.register(Train)
admin.site.register(Alert)
admin.site.register(AlertCard)