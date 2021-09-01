from django import forms

from item.models import Item


class ItemCreateForm(forms.ModelForm):
    class Meta:
        service_id = forms.IntegerField(widget=forms.HiddenInput)
        category_id = forms.IntegerField(widget=forms.HiddenInput)
        quantity = forms.IntegerField(initial=0)
        model = Item
        fields = ('name', 'price', 'description', 'available', 'image')
