from django.contrib import admin

# Register your models here.


from .models import CargoType
from .models import Train
from .models import Alert
from .models import AlertCard
from .models import reasonMaintenance
from .models import Maintenance
from .models import ReasonInspection
from .models import Inspection

admin.site.register(CargoType)
admin.site.register(Train)
admin.site.register(Alert)
admin.site.register(AlertCard)
admin.site.register(reasonMaintenance)
admin.site.register(Maintenance)
admin.site.register(ReasonInspection)
admin.site.register(Inspection)