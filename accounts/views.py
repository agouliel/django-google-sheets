from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from sim.services import *
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class SignupPageView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def signup_view(request):
    if request.method == 'POST':        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User(username=form.cleaned_data['username'])
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            create_worksheets('db', form.cleaned_data['username'])
            return redirect('photo-wall')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
