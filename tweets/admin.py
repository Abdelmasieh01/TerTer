from django.contrib import admin
from .models import CommentTweet, Tweet

# Register your models here.
admin.site.register(Tweet)
admin.site.register(CommentTweet)