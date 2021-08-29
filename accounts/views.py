from django.views.generic import FormView
from accounts.forms import CustomerLoginRegisterForm
from accounts.models import Customer


class CustomerLoginRegisterView(FormView):
    form_class = CustomerLoginRegisterForm
    template_name = None

    def form_valid(self, form):
        try:
            Customer.objects.get(phone_number=form.changed_data['phone_number'])
        except Customer.DoesNotExist:
            self.success_url = None
        else:
            self.success_url = None

        return super().form_valid(form)
