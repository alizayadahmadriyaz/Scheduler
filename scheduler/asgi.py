"""
ASGI config for scheduler project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from schdule import routing

from django.urls import path,include

# application = get_asgi_application()


# from django.urls import re_path
# from schdule.consumers import ChatConsumer

# websocket_urlpatterns = [
#     path(r"ws/chat/", ChatConsumer.as_asgi()),
# ]




# os.environ['DJANGO_SETTINGS_MODULE'] = 'scheduler.settings'
# import django
# django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

