from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Count

from accounts.forms import UserRegisterForm
from job_site_app.models import Company, Specialty


class MySignupView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


