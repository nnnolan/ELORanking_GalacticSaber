from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.

def home(request):
    return render(request, "main/home.html")


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    
    return render(request, 'registration/signup.html', {'form': form})
        