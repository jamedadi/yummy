from django import forms

from item.models import Item


class ItemCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=0)

    class Meta:
        model = Item
        fields = ('name', 'price', 'description', 'available', 'image')


class ItemUpdateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=0)

    class Meta:
        model = Item
        fields = ('category', 'name', 'price', 'description', 'available', 'image')
