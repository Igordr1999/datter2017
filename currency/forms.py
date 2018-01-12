from django import forms
from .models import Valuta, ValutaValue


class ConverterForm(forms.Form):
    #from_valuta = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'special'}))
    #to_valuta = forms.CharField(max_length=3)
    #from_value = forms.FloatField()
    valuta_from = forms.ModelChoiceField(Valuta.objects.all(), widget=forms.Select(attrs={'class': 'uk-select'}))
    valuta_to = forms.ModelChoiceField(Valuta.objects.all(), widget=forms.Select(attrs={'class': 'uk-select'}))
    value_from = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'uk-input'}))
