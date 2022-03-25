<<<<<<< Updated upstream
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import NewUserForm

def signup(request):

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home') #index 
        
    else:
            form = NewUserForm()
    return render(request, 'signup.html', {'form': form})
=======
from django.urls import path
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello, world. You're at the galaticsaber index.")
>>>>>>> Stashed changes
