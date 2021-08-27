from django.contrib import admin

from cart.models import Cart, CartLine


class CartLineInline(admin.TabularInline):
    model = CartLine
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('customer__phone_number',)
    inlines = [CartLineInline]
