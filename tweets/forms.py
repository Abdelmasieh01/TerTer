from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Tweet, CommentTweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('text', 'img',)
        labels = {
            'img': _(''),
        }

    text = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "What's Happening..",}
    ))

class CommentTweetForm(forms.ModelForm):
    class Meta:
        model = CommentTweet
        fields = ('text',)


    text = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Comment on this..', 'rows':1}
    ))
    