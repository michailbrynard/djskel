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
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = ['alpha2code', 'name', 'native_name', 'display_name', 'continent', 'population']
    list_filter = ['continent', 'region']
    search_fields = ['name', 'native_name', 'continent__name', 'region__name', 'alpha2code', 'display_name']


class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


class SubRegionAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code', 'symbol']
    list_display = ['code', 'name', 'symbol']
    fields = ['code', 'name', 'symbol']


# REGISTER
# ---------------------------------------------------------------------------------------------------------------------#
admin.site.register(Country, CountryAdmin)
admin.site.register(Continent, RegionAdmin)
admin.site.register(Region, SubRegionAdmin)
admin.site.register(Currency, CurrencyAdmin)