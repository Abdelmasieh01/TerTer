# Generated by Django 4.0.3 on 2022-04-08 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_alter_commenttweet_img_alter_tweet_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commenttweet',
            name='img',
        ),
    ]