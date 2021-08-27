from django.contrib import admin
from .models import Service, ServiceCategory, DeliveryArea, ServiceAvailableTime, AvailableTime


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'service_type', 'minimum_purchase', 'address')
    list_filter = ('service_type',)
    search_fields = ('name',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'service')
    search_fields = ('name', 'service')


@admin.register(DeliveryArea)
class DeliveryAreaAdmin(admin.ModelAdmin):
    list_display = ('service', 'area')
    search_fields = ('service', 'area')


@admin.register(ServiceAvailableTime)
class ServiceAvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('service', 'available_time')
    list_filter = ('available_time',)
    search_fields = ('service',)


@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('day', 'open_time', 'close_time', 'close_day')
    list_filter = ('day', 'close_time')
