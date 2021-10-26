from django.contrib import admin

from item.models import Item, ItemLine


class ItemLineInline(admin.TabularInline):
    model = ItemLine
    max_num = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'upc', 'service', 'category', 'price', 'stock', 'available')
    list_editable = ('available',)
    list_filter = ('available', 'created_time')
    search_fields = ('upc', 'name')
    inlines = [ItemLineInline]