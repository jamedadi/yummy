from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test as user_test
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from accounts.forms import CustomerLoginRegisterForm, CustomerCodeConfirmForm, CustomerPasswordForm, \
    CustomerPasswordSetForm, ServiceProviderRegistrationForm, ServiceProviderLoginForm, CustomerProfileUpdateForm
from accounts.models import Customer
from accounts.utils import check_expire_time, set_phone_number_session, check_is_not_authenticated, \
    IsCustomer, IsServiceProvider
from library.utils import CustomUserPasses


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerProfileView(IsCustomer, TemplateView):
    template_name = 'accounts/customer/profile.html'


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(user_test(check_is_not_authenticated, login_url=reverse_lazy('accounts:customer-profile')),
                  name='dispatch')
class CustomerLoginRegisterView(FormView):
    form_class = CustomerLoginRegisterForm
    template_name = 'accounts/customer/login_register.html'
    success_url = reverse_lazy('accounts:customer-code-confirm')

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        try:
            customer = Customer.objects.get(phone_number=phone_number)
        except Customer.DoesNotExist:
            set_phone_number_session(self.request, phone_number)
        else:
            if customer.password:
                self.success_url = reverse_lazy('accounts:customer-password-confirm')
                self.request.session['phone_number'] = phone_number
            else:
                set_phone_number_session(self.request, phone_number)

        return super().form_valid(form)


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(user_test(check_is_not_authenticated, login_url=reverse_lazy('accounts:customer-profile')),
                  name='dispatch')
class CustomerPhoneNumberConfirmView(FormView):
    form_class = CustomerCodeConfirmForm
    template_name = 'accounts/customer/phone_number_confirm.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def dispatch(self, request, *args, **kwargs):
        check_expire_time(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        form_code = int(form.cleaned_data['code'])
        session_code = self.request.session.get('code', None)

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
                return redirect('accounts:customer-code-confirm')
        else:
            messages.info(self.request, 'The code is invalid! Enter your phone number again', 'danger')
            return redirect('accounts:customer-login-register')

    def delete_confirm_code(self):
        del self.request.session['code']


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(user_test(check_is_not_authenticated, login_url=reverse_lazy('accounts:customer-profile')),
                  name='dispatch')
class CustomerPasswordConfirmView(FormView):
    form_class = CustomerPasswordForm
    template_name = 'accounts/customer/password_confirm.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        password = form.cleaned_data['password']
        customer = authenticate(phone_number=phone_number, password=password)

        if customer:
            login(self.request, customer)
            messages.info(self.request, 'Login success', 'success')
            return super().form_valid(form)

        else:
            messages.info(self.request, 'Your password is incorrect!', 'danger')
            return redirect('accounts:customer-password-confirm')


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerSetPasswordView(CustomUserPasses, UpdateView):
    model = Customer
    form_class = CustomerPasswordSetForm
    success_url = reverse_lazy('accounts:customer-login-register')
    template_name = 'accounts/customer/password_set.html'

    def test_func(self):
        if not isinstance(self.request.user, Customer):
            return False
        if self.request.user.password:
            return False, True, reverse_lazy("accounts:customer-change-password")

        return True

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerProfileUpdateView(IsCustomer, UpdateView):
    model = Customer
    form_class = CustomerProfileUpdateForm
    success_url = reverse_lazy('accounts:customer-profile')
    template_name = 'accounts/customer/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class CustomerChangePasswordView(CustomUserPasses, PasswordChangeView):
    template_name = 'accounts/customer/change_password.html'
    success_url = reverse_lazy('accounts:customer-profile')

    def test_func(self):
        if not isinstance(self.request.user, Customer):
            return False
        if not self.request.user.password:
            return False, True, reverse_lazy("accounts:customer-set-password")
        return True


class CustomerLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:customer-login-register')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next_page = self.get_next_page()
        response = HttpResponseRedirect(next_page)
        if request.COOKIES.get('cart_id', None) is not None:
            response.delete_cookie('cart_id')
        return response


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
@method_decorator(user_test(check_is_not_authenticated, login_url=reverse_lazy('accounts:service-provider-profile')),
                  name='dispatch')
class ServiceProviderRegistrationView(FormView):
    form_class = ServiceProviderRegistrationForm
    template_name = 'accounts/service_provider/registration.html'
    success_url = reverse_lazy('accounts:service-provider-login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.password = make_password(instance.password)
        instance.save()
        return super().form_valid(form)


@method_decorator(require_http_methods(['POST', 'GET']), name='dispatch')
@method_decorator(user_test(check_is_not_authenticated, login_url=reverse_lazy('accounts:service-provider-profile')),
                  name='dispatch')
class ServiceProviderLoginView(FormView):
    form_class = ServiceProviderLoginForm
    template_name = 'accounts/service_provider/login.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        user_authenticated = authenticate(username=user.username, password=user.password)
        if user_authenticated:
            login(self.request, user_authenticated)
        return super().form_valid(form)


@method_decorator(require_http_methods(['GET']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ServiceProviderProfileView(IsServiceProvider, TemplateView):
    template_name = 'accounts/service_provider/profile.html'
    raise_exception = True


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(login_required(login_url=reverse_lazy('accounts:customer-login-register')), name='dispatch')
class ServiceProviderChangePasswordView(IsServiceProvider, PasswordChangeView):
    template_name = 'accounts/service_provider/change_password.html'
    success_url = reverse_lazy('accounts:service-provider-profile')
