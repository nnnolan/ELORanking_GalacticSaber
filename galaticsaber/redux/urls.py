"""redux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reduxapp import views

urlpatterns = [
    # User handling
    path('admin/', admin.site.urls),
    path('create/', views.createuser, name="createuser"),

    # Data creation
    path('', views.home, name="home"),

    # Data visualization
    # path('ranking/', views.ranking, name="ranking"),
    path('player/', views.playersearch, name="playersearch"),
    path('player/<int:user_pk>', views.playerpage, name='playerpage'),
    # path('dataToVisualization/<int:user_pk>', views.dataToVisuals, name="dataToVisuals"),

]
