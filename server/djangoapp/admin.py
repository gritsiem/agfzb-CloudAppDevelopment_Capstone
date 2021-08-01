from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
   model = CarModel
# CarModelAdmin class

class CarModelAdmin(admin.ModelAdmin):
   model = CarModel

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel,CarModelAdmin)