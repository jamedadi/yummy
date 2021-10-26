from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('customer__phone_number',)
