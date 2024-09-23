from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(products)
admin.site.register(addcart)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ['order_id', 'user', 'total_amount', 'created_at']