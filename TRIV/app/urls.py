from django.urls import path
from . import views
from . import routing  # Import your routing file

urlpatterns = [
    path('', views.index, name='index'),  # Existing HTTP route
] + routing.websocket_urlpatterns  # Add the WebSocket URL patterns
