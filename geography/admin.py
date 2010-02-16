from django.contrib import admin
from olwidget.admin import GeoModelAdmin
from geography.models import Location

class LocationAdmin(GeoModelAdmin):
    options= {
        'layers':['osm.mapnik','google.satellite']
    }
admin.site.register(Location,LocationAdmin)