from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['CATname','CATparent']

class ProductsImageAdmin(admin.StackedInline):
    model = models.ProductsImage
    extra = 4

@admin.register(models.Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductsImageAdmin]

@admin.register(models.Product_Alternative)
class Product_AlternativeAdmin(admin.ModelAdmin):
    list_display =['PlaneA_product']
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =['user']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display =['product','qunatity']

@admin.register(models.ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display =[]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =['user','product']
