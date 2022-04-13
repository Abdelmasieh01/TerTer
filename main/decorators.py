from django.shortcuts import redirect
from functools import wraps
from .models import MyUser

def has_profile(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            profile = MyUser.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        except:
            return redirect('main:set_profile')
    return wrap