from django.contrib import admin
from .models import AdvUser, Transfers, Currency


class TransfersAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'account', 'amount', 'transfer_type',)


admin.site.register(Currency)
admin.site.register(AdvUser)
admin.site.register(Transfers, TransfersAdmin)
# Register your models here.
