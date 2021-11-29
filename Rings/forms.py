from django import forms
from .models import Ring


class RingForm(forms.ModelForm):

    class Meta:
        model = Ring
        fields = ['bezeichnung', 'preis', 'material', 'ring_Breite']
        widgets = {
            'genre': forms.Select(choices=Ring.RING_MATERIALS),
            'user': forms.HiddenInput(),
        }
