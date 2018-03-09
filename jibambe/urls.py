"""jibambeApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from movies import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moviescategories/', views.MoviesCategoriesList.as_view()),
    path('moviescategories/<pk>', views.MovieCategoryDetails.as_view()),
    path('series/', views.SeriesList.as_view()),
    path('series/<pk>', views.SingleSeries.as_view()),
    path('episodes/<pk>', views.Episodes.as_view()),
    path('topupaccount/', accounts_views.AccountTopUp.as_view()),
    path('login/', accounts_views.UserLogin.as_view()),
    path('users/', accounts_views.Users.as_view())
]
