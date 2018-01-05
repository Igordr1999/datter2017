from django.contrib import admin
from currency.models import Valuta, ValutaValue

# Register your models here.
admin.site.register(Valuta)


@admin.register(ValutaValue)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['valuta', 'date', 'value']

