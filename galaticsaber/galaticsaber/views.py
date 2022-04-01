from django.shortcuts import render

def my_view(request):
    return render("i hate this website and especially you", request)

def leaderboard(request):
    return render(request, "login/leaderboard.html")