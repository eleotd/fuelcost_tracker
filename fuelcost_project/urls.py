"""
URL configuration for fuelcost_project project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views
from tracker import views as tracker_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', tracker_views.home, name='home'),
    
    # Пользователи
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    
    # Трекер
    path('dashboard/', tracker_views.dashboard, name='dashboard'),
    path('refuels/', tracker_views.refuel_list, name='refuel-list'),
    path('refuels/add/', tracker_views.refuel_add, name='refuel-add'),
    path('refuels/<int:pk>/edit/', tracker_views.refuel_edit, name='refuel-edit'),
    path('refuels/<int:pk>/delete/', tracker_views.refuel_delete, name='refuel-delete'),
    path('cars/', tracker_views.car_list, name='car-list'),
    path('cars/add/', tracker_views.car_add, name='car-add'),
    path('statistics/', tracker_views.statistics, name='statistics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)