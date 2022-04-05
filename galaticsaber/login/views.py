import math

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
# from .models import Player, mtg_duel, lsd_duel
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "login/home.html")

def leaderboard(request):
    return render(request, "login/leaderboard.html")

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/signup.html', {'form': form})
    

# def forgot_password(request):
#     return render(request, "login/forgot-password.html")


# @login_required
# def player(request)