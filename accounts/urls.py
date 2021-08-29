from django.urls import path
from accounts.views import CustomerLoginRegisterView, CustomerPhoneNumberConfirmView, CustomerPasswordConfirmView, \
    ProfileView

app_name = 'accounts'

urlpatterns = [
    path('login-register/', CustomerLoginRegisterView.as_view(), name='login-register'),
    path('code-confirm/', CustomerPhoneNumberConfirmView.as_view(), name='code-confirm'),
    path('password-confirm/', CustomerPasswordConfirmView.as_view(), name='password-confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
