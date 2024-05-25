from django.contrib import admin

from core.apps.products.models import Product
from core.apps.products.models.reviews import Review


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_visible')
    inlines = (ReviewInLine,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product')
    list_select_related = ('customer', 'product')
