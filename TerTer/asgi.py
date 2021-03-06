import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tweets.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TerTer.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tweets.routing.ws_urlpatterns
        )
    )
})
