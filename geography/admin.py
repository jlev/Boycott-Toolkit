from django.contrib import admin
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete

from geography.models import Map

class MapAdmin(admin.ModelAdmin):
    tags = TagField(widget=TagAutocomplete(), required=False)
    class Meta:
        model = Map
    
admin.site.register(Map,MapAdmin)