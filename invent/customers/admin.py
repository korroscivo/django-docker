from django.contrib import admin

from customers.models import Client, CustomUser
from tenant_schemas.models import TenantMixin


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
        list_display = ('name', 'paid_until')




admin.site.register(CustomUser)