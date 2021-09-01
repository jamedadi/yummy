from django import forms

from item.models import Item
from service.models import ServiceCategory


class ItemCreateForm(forms.ModelForm):
    quantity = forms.IntegerField(initial=0)

    class Meta:
        model = Item
        fields = ('name', 'price', 'description', 'available', 'image')


def item_update_form_factory(service=None):
    class ItemUpdateForm(forms.ModelForm):
        quantity = forms.IntegerField(initial=0)

        class Meta:
            model = Item
            fields = ('category', 'name', 'price', 'description', 'available', 'image')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if service:
                self.fields['category'].queryset = ServiceCategory.objects.filter(service=service)

    return ItemUpdateForm
