from django.views.generic import FormView

from item.forms import ItemCreateForm
from item.models import Item


class CreatItemView(FormView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/create_form.html'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.service_id = form.cleaned_data['service_id']
        item.category_id = form.cleaned_data['category_id']
        item.line.quantity += form.cleaned_data['quantity']
        item.save()
        return super().form_valid(form)
