from django.urls import path
from . import views

app_name='tweets'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
    path('tweets/<int:tweet_id>/', views.tweet_view, name='tweet'),
]