"""
ASGI config for d08 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d08.settings")

# This is the standard Django ASGI application for HTTP requests.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # HTTP requests are handled by the default Django ASGI application.
        "http": django_asgi_app,
        # WebSocket connections are handled by our own routing.
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)
