"""
URL configuration for WalletWatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register , name='register' ),
    path('login/', login_views , name='login'),
    path('home/', home_views , name='home_views'),
    path('logout/', logout_views , name='logout'),
    path('add_expense/', add_expense , name='add_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense , name='edit_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense , name='delete_expense'),
    path('charts/',charts  , name='charts'),

]
