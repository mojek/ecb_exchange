from django.contrib import admin
from .models import Currency, Exchange


class ExchangeInline(admin.TabularInline):
    model = Exchange


class CurrencyAdmin(admin.ModelAdmin):
    inlines = [ExchangeInline]


admin.site.register(Currency, CurrencyAdmin)
