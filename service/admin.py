from django.contrib import admin
from .models import Service, ServiceCategory, DeliveryArea, ServiceAvailableTime


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
    list_display = ('service', 'day', 'open_time', 'close_time', 'is_close')
    list_filter = ('day', 'is_close')
    search_fields = ('service',)


