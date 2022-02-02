from django import forms
from django.forms import Textarea

from .models import Ring


class RingForm(forms.ModelForm):
    product_img_url = forms.ImageField(required=True)

    class Meta:
        model = Ring

        fields = ['material', 'bezeichnung', 'preis', 'category', 'ring_size', 'product_img_url', 'description']
        widgets = {
            'material': forms.Select(choices=Ring.RING_MATERIALS),
            'description': Textarea()
        }
