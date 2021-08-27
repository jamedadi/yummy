from django.contrib import admin

from item.models import Item


@admin.register(Item)
class Item(admin.ModelAdmin):
    list_display = ('name', 'upc', 'price', 'stock', 'available')
    list_editable = ('available',)
    list_filter = ('available', 'created_time')
    search_fields = ('upc', 'name')
