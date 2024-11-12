from django.urls import path
from . import consumers

# Define WebSocket URL patterns for routing WebSocket connections
websocket_urlpatterns = [
    # Route WebSocket connections to ChatConsumer based on room_name
    # Format: ws://<domain>/ws/<room_name>/
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi())
]