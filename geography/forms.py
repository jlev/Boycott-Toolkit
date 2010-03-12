from django import forms
from tagging.forms import TagField
from autocomplete.widgets import TagAutocomplete,Autocomplete
from geography.models import Map

class MapInlineForm(forms.ModelForm):
    #tags = TagField(widget=TagAutocomplete(), required=False)
    center = forms.fields.Field(widget=forms.widgets.TextInput()) #override the TextArea default
    class Meta:
        model = Map