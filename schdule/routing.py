from django.urls import path,re_path
from schdule.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+_\w+)/$", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)