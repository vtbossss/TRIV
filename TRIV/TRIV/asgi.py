import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing  # Your app's custom routing file for WebSockets

# Set the default settings module for the 'asgi' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRIV.settings")

# Define the ASGI application to handle HTTP and WebSocket connections
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": URLRouter(app.routing.websocket_urlpatterns),  # Handles WebSocket connections
})
