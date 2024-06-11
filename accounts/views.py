from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
# Create your views here.
def home(request):
    return render(request,'./accounts/home.html')


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save() # forms.py save function ke call kore user data ana holo
        login(self.request,user)
        print(user)
        return super().form_valid(form) # form valid func call hobe autometic

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    

class UserLogoutView(LogoutView):

    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)

        return reverse_lazy('home')


