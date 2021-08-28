from django.contrib import admin
from .models import State, City, Area, Address


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'state')
    list_filter = ('state',)
    search_fields = ('name',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'city')
    list_filter = ('city',)
    search_fields = ('name',)


@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ('state', 'city', 'area', 'floor', 'plaque')
    list_filter = ('state', 'city')
    search_fields = ('area', 'floor', 'plaque')
