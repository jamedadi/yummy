from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from accounts.models import Customer, ServiceProvider


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('phone_number',)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('phone_number',)
    search_fields = UserAdmin.search_fields + ('phone_number',)
    fieldsets = UserAdmin.fieldsets + (
        (_("Phone number"), {'fields': ('phone_number',)}),
    )
