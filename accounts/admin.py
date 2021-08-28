from django.contrib import admin


from accounts.models import Customer, ServiceProvider


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('phone_number',)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'phone_number')
