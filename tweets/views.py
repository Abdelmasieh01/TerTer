from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from main.models import MyUser
from main.decorators import has_profile
from .forms import TweetForm, CommentTweetForm
from .models import Tweet, CommentTweet

#@has_profile
def index(request):
    tweets = Tweet.objects.all()    
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, user=request.user)

        if profile.follows.all():
            tweets = Tweet.objects.filter(user=profile)
            for follow in profile.follows.all():
                followed_by_me = MyUser.objects.get(user=follow)
                tweets |= Tweet.objects.filter(user=followed_by_me).order_by('-date',)

        if request.method == 'POST':
            if 'post' in request.POST:
                form = TweetForm(request.POST, request.FILES)
                if form.is_valid():
                    text = form.cleaned_data.get('text')
                    if request.FILES:
                        img = request.FILES['img']
                        tweet = Tweet(user=profile, tweet=text, img=img)
                        tweet.save()
                    else:
                        tweet = Tweet(user=profile, tweet=text)
                        tweet.save()

            elif 'comment' in request.POST:
                comment_form = CommentTweetForm(request.POST)
                if comment_form.is_valid():
                    text = comment_form.cleaned_data.get('text')
                    tweet_id = request.POST.get('tweet-id', "")
                    tweet = Tweet.objects.get(pk=tweet_id)
                    tweet.comments += 1
                    tweet.save()
                    comment_tweet = CommentTweet(user=profile, comment_tweet=text, tweet=tweet)
                    comment_tweet.save()
                    
        form = TweetForm()
        comment_form = CommentTweetForm()
        return render(request, 'index.html', {'form': form, 'comment_form': comment_form, 'profile': profile, 'tweets': tweets})
    
    return render(request, 'login_or_signup.html')

@login_required(login_url='/login/')
#@has_profile
def profile(request, username):
    profile = get_object_or_404(MyUser, Q(user__username=username))
    logged_in_profile = get_object_or_404(MyUser, user=request.user)
    tweets = Tweet.objects.filter(user=profile).order_by('-date')
    if request.method == 'POST':
        form = CommentTweetForm(request.POST)
        if form.is_valid():
            comment_tweet_text = form.cleaned_data.get('text')
            tweet_id = request.POST.get('tweet-id')
            tweet = Tweet.objects.get(pk=tweet_id)
            tweet.comments += 1
            tweet.save()
            comment_tweet = CommentTweet(user=logged_in_profile, comment_tweet=comment_tweet_text, tweet=tweet)
            comment_tweet.save()

    mine = logged_in_profile == profile
    followed = profile.user in logged_in_profile.follows.all()
    print(followed)
    form = CommentTweetForm()
    return render(request, 'tweets/profile.html', {'mine': mine, 
    'profile': profile, 'logged_in': logged_in_profile, 'tweets': tweets,
    'form': form, 'followed': followed})

@login_required(login_url='/login/')
#@has_profile
def tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    profile = MyUser.objects.get(user=request.user)
    comments = CommentTweet.objects.filter(tweet=tweet)
    if request.method == 'POST':
        form = CommentTweetForm(request.POST)
        if form.is_valid():
            comment_tweet_text = form.cleaned_data.get('text')
            tweet_id = request.POST.get('tweet-id')
            tweet = Tweet.objects.get(pk=tweet_id)
            comment_tweet = CommentTweet(user=profile, comment_tweet=comment_tweet_text, tweet=tweet)
            comment_tweet.save()
    
    form = CommentTweetForm()
    return render(request, 'tweets/tweet.html', {'profile': profile,
    'tweet': tweet, 'form': form, 'comments': comments})

@login_required(login_url='/login/')
#@has_profile
def follow(request, username):
    logged_in = MyUser.objects.get(user=request.user)
    profile = MyUser.objects.get(Q(user__username=username))
    if profile.user in logged_in.follows.all():
        logged_in.follows.remove(profile.user)
        profile.followers -= 1
    else:
        logged_in.follows.add(profile.user)
        profile.followers += 1
    return redirect('tweets:profile', username=username)


### Earlier version of code ###

# @login_required(login_url='/login/')
# @has_profile
# def tweet_like(request, tweet_id):
#     tweet = get_object_or_404(Tweet, pk=tweet_id)
#     profile = MyUser.objects.get(user=request.user)
#     like, created = Like.objects.get_or_create(user=profile, tweet=tweet)
#     if not created:
#         tweet.likes -= 1
#         like.delete()
#     else:
#         like.save()
#         tweet.likes += 1
#         tweet.save()

# @login_required(login_url='/login/')
# @has_profile
# def comment_like(request, comment_id):
#     comment = get_object_or_404(CommentTweet, pk=comment_id)
#     profile = MyUser.objects.get(user=request.user)
#     like, created = Like.objects.get_or_create(user=profile, tweet=comment)
#     if not created:
#         comment.likes -= 1
#         comment.save()
#         like.delete()
#     else:
#         comment.likes += 1
#         comment.save()
    