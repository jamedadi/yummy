from django import forms

from item.models import Item
from service.models import ServiceCategory


class ItemCreateForm(forms.ModelForm):
    class Meta:
        quantity = forms.IntegerField(initial=0)
        model = Item
        fields = ('name', 'price', 'description', 'available', 'image')


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        quantity = forms.IntegerField()
        model = Item
        fields = ('category', 'name', 'price', 'description', 'available', 'image')

    def __init__(self, service=None, *args, **kwargs):
        super().__init__(service, *args, **kwargs)
        if service:
            self.fields['category'].queryset = ServiceCategory.objects.filter(service=service)
