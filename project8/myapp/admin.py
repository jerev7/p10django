from django.contrib import admin
from .models import Category, Products, Product_saved


# Register your models here.
class ProductSavedAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product_saved, ProductSavedAdmin)


class ProductsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Products, ProductsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
