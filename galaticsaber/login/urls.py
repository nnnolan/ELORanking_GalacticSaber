from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='register'),

    # path('register', views.register, name='register'), # register page
]