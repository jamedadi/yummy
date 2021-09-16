from django.contrib import admin

from payment.models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'price', 'is_paid', 'address')
    list_filter = ('is_paid', 'created_time')
    search_fields = ('customer__phone_number',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'customer', 'gateway', 'price', 'is_paid')
    list_filter = ('is_paid', 'created_time', 'gateway')
    search_fields = ('uuid', 'customer__phone_number')
