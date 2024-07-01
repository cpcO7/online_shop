from django.contrib import admin

from apps.models import Category, Product, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
