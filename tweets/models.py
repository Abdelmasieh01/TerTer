from django.db import models
from main.models import MyUser

class Tweet(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=500)
    img = models.ImageField(upload_to='tweets/%Y/%m/%d/', blank=True)
    likes = models.ManyToManyField(MyUser, blank=True, related_name='tweet_likes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username + ' tweeted "' + self.tweet + '"'
    
    def get_likes(self):
        return self.likes.all().count()
    
    def get_comments(self):
        return self.commenttweet_set.all().count()

class CommentTweet(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comment_tweet = models.CharField(max_length=500)
    likes = models.ManyToManyField(MyUser, blank=True, related_name='comment_likes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username + ' commented on ' + self.tweet.user.user.username + "'s tweet."
    
    def get_likes(self):
        return self.likes.all().count()