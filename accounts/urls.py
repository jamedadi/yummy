from django.urls import path
from accounts.views import CustomerLoginRegisterView, CustomerPhoneNumberConfirmView, CustomerPasswordConfirmView, \
    ProfileView

app_name = 'accounts'

urlpatterns = [
    path('customer/login-register/', CustomerLoginRegisterView.as_view(), name='login-register'),
    path('customer/code-confirm/', CustomerPhoneNumberConfirmView.as_view(), name='code-confirm'),
    path('customer/password-confirm/', CustomerPasswordConfirmView.as_view(), name='password-confirm'),
    path('customer/profile/', ProfileView.as_view(), name='profile'),
]
