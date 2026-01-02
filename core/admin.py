from django.contrib import admin
from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'country', 'code', 'is_popular']
    list_filter = ['is_popular', 'state', 'country']
    search_fields = ['name', 'state', 'code']
    list_editable = ['is_popular']
