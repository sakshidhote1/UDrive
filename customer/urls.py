"""udrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from .views import *
from cardealer.views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('aboutus/', aboutus),
    path('contact/', contactus),
    path('customersignup/', customerreg),
    path('registration/', customersignup),
    path('login/', customerlogin),
    path('login_failed/',login_failed),
    path('notapproved/',notapproved,name='notapproved'),
    path('customerdashboard/',customerdashboard,name='customerdashboard'),
    path('customerlogout/', LogoutView.as_view(template_name='customerlogin.html'),name='logout'),

    path('dealerregistration/', dealersignup),
    path('dealerreg/', dealerreg),
    path('deleardashboard/', deleardashboard),
    path('dealerlogin/', dealerlogin),
    path('auth/', auth_view),
    path('dealerlogout/', LogoutView.as_view(template_name='login.html'), name='dealerlogout'),

    path('add_vehicle/', add_vehicle),

    path('manage_vehicles/',manage_vehicles),
    path('order_list/',order_list),
    path('complete/',complete),
    path('history/',history),
    path('delete/<int:id>',delete),

    path('search/', search),
    path('search_results/', search_results),
    path('rent/',rent_vehicle),
    path('confirmed/',confirm),
    path('manage/',manage),
    path('update/',update_order),
    path('delete/',delete_order),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
