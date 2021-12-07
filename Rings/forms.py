from django import forms
from .models import Ring, Comment


class RingForm(forms.ModelForm):

    class Meta:
        model = Ring
        fields = ['bezeichnung', 'preis', 'material', 'ring_Breite']
        widgets = {
            'genre': forms.Select(choices=Ring.RING_MATERIALS),
            'user': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'user': forms.HiddenInput(),
            'book': forms.HiddenInput(),
        }