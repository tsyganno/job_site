from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import MyLoginView, MySignupView


app_name = 'accounts'

urlpatterns = [
    path('signup', MySignupView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
