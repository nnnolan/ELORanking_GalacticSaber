from django.shortcuts import render, redirect
# from django.contrib.auth.models import login, authenticate

# from . import SignUpForm

# Create your views here.
def index(request):
    return render(request, 'login/login.html')

# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})

def register(request):
    return render(request, 'login/register.html')