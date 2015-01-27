# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.contrib import admin
from fact_book.models import Country, Continent, Region, Currency
from logging import getLogger


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# ADMIN
# ---------------------------------------------------------------------------------------------------------------------#
class CountryAdmin(admin.ModelAdmin):
    list_display = ['alpha2code', 'name', 'native_name', 'display_name', 'continent', 'population']
    list_filter = ['continent', 'region']
    search_fields = ['name', 'native_name', 'continent__name', 'region__name', 'alpha2code', 'display_name']


class RegionAdmin(admin.ModelAdmin):
    pass


class SubRegionAdmin(admin.ModelAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    fields = ['code', 'name']


# REGISTER
# ---------------------------------------------------------------------------------------------------------------------#
admin.site.register(Country, CountryAdmin)
admin.site.register(Continent, RegionAdmin)
admin.site.register(Region, SubRegionAdmin)
admin.site.register(Currency, CurrencyAdmin)