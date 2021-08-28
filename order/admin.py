from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'status', 'is_delivered')
    list_filter = ('status', 'is_delivered')
    search_fields = ('invoice',)
