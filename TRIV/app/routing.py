from django.urls import re_path
from .consumers import AgroDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/agro_data/', AgroDataConsumer.as_asgi()),
]
