from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # TODO-1: after done todos the model order, add the fields here
    pass
