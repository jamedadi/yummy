from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from accounts.views import CustomerLoginRegisterView, CustomerPhoneNumberConfirmView, CustomerPasswordConfirmView, \
    CustomerProfileView, CustomerSetPasswordView, ServiceProviderRegistrationView, ServiceProviderLoginView, \
    ServiceProviderProfileView, CustomerProfileUpdateView, CustomerChangePasswordView, \
    ServiceProviderChangePasswordView, CustomerLogoutView

app_name = 'accounts'

urlpatterns = [
    path('customer/login-register/', CustomerLoginRegisterView.as_view(), name='customer-login-register'),
    path('customer/code-confirm/', CustomerPhoneNumberConfirmView.as_view(), name='customer-code-confirm'),
    path('customer/password-confirm/', CustomerPasswordConfirmView.as_view(), name='customer-password-confirm'),
    path('customer/profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('customer/profile-update/', CustomerProfileUpdateView.as_view(), name='customer-profile-update'),
    path('customer/set-password/', CustomerSetPasswordView.as_view(), name='customer-set-password'),
    path('customer/change-password/', CustomerChangePasswordView.as_view(), name='customer-change-password'),
    path('customer/logout/', CustomerLogoutView.as_view(), name='customer-logout'),
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
    path('serviceprovider/profile/', ServiceProviderProfileView.as_view(), name='service-provider-profile'),
    path('serviceprovider/change-password/', ServiceProviderChangePasswordView.as_view(),
         name='service-provider-change-password'),
    path('serviceprovider/logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:service-provider-login')),
         name='service-provider-logout'),
]
