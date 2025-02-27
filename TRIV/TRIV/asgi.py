import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
import app.routing  # Your app's custom routing file for WebSockets
import weather.routing1  # Your weather routing file

# Set the default settings module for the 'asgi' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRIV.settings")

# Define the ASGI application to handle HTTP and WebSocket connections
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": OriginValidator(
        URLRouter(app.routing.websocket_urlpatterns + weather.routing1.websocket_urlpatterns),
        allowed_origins=["*"],  # Allow all origins temporarily (for development)
    ),
})
