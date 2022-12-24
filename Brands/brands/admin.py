from django.contrib import admin
from . import models

@admin.register(models.Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display =['Bname']

    