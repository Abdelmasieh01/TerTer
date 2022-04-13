import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Tweet, MyUser

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'test'
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'You are now connected',
            'username': self.user.username,
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        id = int(text_data_json['tweet_id'])
        count = await self.is_liked(id)
        await self.channel_layer.group_send(
            self.group_name,
            {   
                'type': 'send_like',
                'id': id,
                'count': count
            }  
        )
    
    async def send_like(self, event):     
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'count': event['count']
        }))

    @database_sync_to_async
    def is_liked(self, id):
        tweet = Tweet.objects.get(id=id)
        profile = MyUser.objects.get(user=self.user)
        if profile in tweet.likes.all():
            tweet.likes.remove(profile)
        else:
            tweet.likes.add(profile)        
        return  tweet.likes.all().count()
