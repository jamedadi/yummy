from django.contrib import admin

from gateway.models import Gateway


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('title', 'gateway_code', 'is_enable')
    list_filter = ('is_enable',)
    search_fields = ('title',)

