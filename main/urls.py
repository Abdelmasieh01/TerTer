from django.urls import path
from . import views

app_name = 'main'

urlpatterns=[
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('register/', views.register, name='register'),
    path('set-profile/', views.set_profile, name='set_profile'),
    path('settings/change-password', views.change_password, name='change_password'),
]