from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('home', views.home, name="home"),
    path('sign-up', views.signup, name="sign_up"),
    path('forgot-password', views.home, name="forgot_password"),
    path('leaderboard', views.leaderboard, name="leaderboard"),
    path(r'^game/new/$', views.new_game, name="new_game"),
]