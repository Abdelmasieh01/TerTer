from django.contrib import admin
from .models import MyUser 

admin.site.site_header = 'TerTer'
admin.site.index_title = 'Administration'
admin.site.site_title = 'TerTer'

admin.site.register(MyUser)