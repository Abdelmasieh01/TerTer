from django.contrib import admin
from django.urls import path, include
#Mdeia imports
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('tweets.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)