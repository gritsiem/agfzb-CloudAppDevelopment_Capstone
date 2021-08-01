from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
   model = CarModel
# CarModelAdmin class


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    inline = [CarModelInline]

# Register models here
admin.site.register(CarMake,CarMakeAdmin)
admin.site.register(CarModel)