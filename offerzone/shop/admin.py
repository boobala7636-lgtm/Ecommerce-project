from django.contrib import admin
from . import models
# Register your models here.


class CatagoryAdmmin(admin.ModelAdmin):
    list_display = ('name','image','description')
    
admin.site.register(models.Catagory,CatagoryAdmmin)
admin.site.register(models.Product)