from django.urls import path
from . import views
from . import routing1  # Import your routing file

urlpatterns = [
    path('', views.weather_by_coordinates),
    path('test/',views.weather_test)
]+ routing1.websocket_urlpatterns  # Add the WebSocket URL patterns
