from django.contrib import admin
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete

from geography.models import Location

class LocationAdmin(admin.ModelAdmin):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta():
        model = Location
    
admin.site.register(Location,LocationAdmin)