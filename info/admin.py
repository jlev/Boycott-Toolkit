from django.contrib import admin
from django import forms
from info.models import Source,Citation
from info.forms import SourceForm,CitationForm

class SourceAdmin(admin.ModelAdmin):
    form = SourceForm

class CitationAdmin(admin.ModelAdmin):
    form = CitationForm

admin.site.register(Source,SourceAdmin)
admin.site.register(Citation,CitationAdmin)