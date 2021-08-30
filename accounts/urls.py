from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from accounts.views import CustomerLoginRegisterView, CustomerPhoneNumberConfirmView, CustomerPasswordConfirmView, \
    ProfileView, CustomerSetPasswordView, ServiceProviderRegistrationView, ServiceProviderLoginView, \
    ServiceProviderProfileView, CustomerProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('customer/login-register/', CustomerLoginRegisterView.as_view(), name='customer-login-register'),
    path('customer/code-confirm/', CustomerPhoneNumberConfirmView.as_view(), name='customer-code-confirm'),
    path('customer/password-confirm/', CustomerPasswordConfirmView.as_view(), name='customer-password-confirm'),
    path('customer/profile/', ProfileView.as_view(), name='customer-profile'),
    path('customer/<int:pk>/profile-update/', CustomerProfileUpdateView.as_view(), name='customer-profile-update'),
    path('customer/<int:pk>/set-password/', CustomerSetPasswordView.as_view(), name='customer-set-password'),
    path('customer/logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:customer-login-register')),
         name='customer-logout'),
    path(
        'serviceprovider/registration/', ServiceProviderRegistrationView.as_view(), name='service-provider-registration'
    ),
    path('serviceprovider/login/', ServiceProviderLoginView.as_view(), name='service-provider-login'),
    path('serviceprovider/profile/', ServiceProviderProfileView.as_view(), name='service-provider-profile'),
    path('serviceprovider/logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:service-provider-login')),
         name='service-provider-logout'),
]
