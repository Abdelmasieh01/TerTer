from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    follows = models.ManyToManyField(User, blank=True, related_name='follows')
    followers = models.IntegerField(default=0)
    pp = models.ImageField(upload_to='main', blank=True)

    def __str__(self):
        return self.user.username

    def get_follows(self):
        return self.follows.all().count()

