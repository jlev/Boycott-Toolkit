from django import forms
from autocomplete.widgets import EntryAutocomplete
from info.models import Citation,Source

class CitationForm(forms.ModelForm):
    class Meta:
        model = Citation

class SourceForm(forms.ModelForm):
    name = forms.fields.CharField(widget=EntryAutocomplete(attrs={'model':'info.source','field':'name'}), required=False)
    author = forms.fields.CharField(widget=EntryAutocomplete(attrs={'model':'info.source','field':'author'}), required=False)
    
    class Meta:
        model = Source