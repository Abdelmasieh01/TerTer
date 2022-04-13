from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import MyUser

class NewUserForm(UserCreationForm):
    
    #Adding the email field, UserCreationForm doesn't have it
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}), required=True)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}), 
    help_text="Password must contain 8 characters. Password Can't be all numbers.")
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    #Defining meta class containing User model and fields in the form
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'first_name': _(''),
            'last_name': _(''),
            'username': _(''),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
        
    
    #Changing original save method to save email
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewAuthForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields=('pp',)

