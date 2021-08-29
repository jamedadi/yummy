from django.contrib import messages
from django.views.generic import FormView
from accounts.forms import CustomerLoginRegisterForm, CustomerCodeConfirmForm, CustomerPasswordForm
from accounts.models import Customer
from accounts.utils import check_expire_time
from django.contrib.auth import authenticate, login


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


class CustomerPhoneNumberConfirmView(FormView):
    form_class = CustomerCodeConfirmForm
    template_name = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        check_expire_time(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phone_number = '98' + self.request.session['phone_number']
        form_code = int(form.changed_data['code'])
        session_code = self.request.get('code', None)

        if session_code:
            if session_code == form_code:
                Customer.objects.get_or_create(phone_number=phone_number)
                self.delete_confirm_code()
                customer = authenticate(phone_number=phone_number)
                if customer:
                    login(self.request, customer)
                    messages.info(self.request, 'Login success', 'success')
                    return super().form_valid(form)
                else:
                    return super().form_valid(form)

            else:
                messages.info(self.request, 'The code is incorrect!', 'danger')
                return
        else:
            messages.info(self.request, 'The code is invalid! Enter your phone number again', 'danger')
            return

    def delete_confirm_code(self):
        del self.request.session['code']


class CustomerPasswordConfirmView(FormView):
    form_class = CustomerPasswordForm
    template_name = None
    success_url = None

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        password = form.changed_data['password']
        customer = authenticate(phone_number=phone_number, password=password)

        if customer:
            login(self.request, customer)
            messages.info(self.request, 'Login success', 'success')
            super().form_valid(form)

        else:
            messages.info(self.request, 'Your password is incorrect!', 'danger')
            return
