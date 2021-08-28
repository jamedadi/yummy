from django.contrib import admin

from payment.models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'price', 'is_paid', 'address')
    list_filter = ('is_paid', 'crated_time')
    search_fields = ('customer__phone_number',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'price', 'is_paid')
    list_filter = ('is_paid', 'created_time')
    search_fields = ('uuid',)
