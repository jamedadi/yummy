from django.urls import path
from accounts.views import CustomerLoginRegisterView, CustomerPhoneNumberConfirmView, CustomerPasswordConfirmView, \
    ProfileView, CustomerSetPasswordView

app_name = 'accounts'

urlpatterns = [
    path('customer/login-register/', CustomerLoginRegisterView.as_view(), name='customer-login-register'),
    path('customer/code-confirm/', CustomerPhoneNumberConfirmView.as_view(), name='customer-code-confirm'),
    path('customer/password-confirm/', CustomerPasswordConfirmView.as_view(), name='customer-password-confirm'),
    path('customer/profile/', ProfileView.as_view(), name='customer-profile'),
    path('customer/<int:pk>/set-password/', CustomerSetPasswordView.as_view(), name='customer-set-password'),

]
