from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import NewAuthForm
from django.contrib.auth.decorators import login_required
from .models import MyUser
from .forms import ProfileForm
#REST API
# from rest_framework import viewsets, permissions
# from .serializers import UserSerializer, GroupSerializer


def mylogin(request):
    if request.method == 'POST':
        #Making an authentication form and checking it is valid
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #authenticate returns User object if username and password are correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                #login if everything is correct
                login(request, user)
                return redirect('tweets:index')
            else:
                return render(request, 'main/login.html', {'form': form})
        
        else:
            return render(request, 'main/login.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('tweets:index')    
    form = NewAuthForm()
    return render(request, 'main/login.html', {'form': form})

@login_required(login_url='/login/')
def mylogout(request):
    logout(request)
    return redirect('tweets:index')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:set_profile')
        else:
            return render(request, 'main/register.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('tweets:index')
    form = NewUserForm()
    return render(request, 'main/register.html', {'form': form})

@login_required(login_url='/login/')
def set_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_pic = request.FILES['pp']
            profile, created = MyUser.objects.get_or_create(user=request.user)
            profile.pp = profile_pic
            profile.save()
            return redirect('tweets:index')
        else:
            return render(request, 'main/set_pp.html', {'form': form})
    form = ProfileForm()
    return render(request, 'main/set_pp.html', {'form': form})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('tweets:index')
            
    form = PasswordChangeForm(request.user)
    return render(request, 'main/change_pass.html', {'form': form})


        
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
