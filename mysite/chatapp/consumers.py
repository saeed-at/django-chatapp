from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage
from cryptography.fernet import Fernet
from django.conf import settings


#! fix: if the user sends a messae with just spaces, it will be saved in the ddatabse, it should not, i this casw just show an alarm!
class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat functionality.
    Manages connections, message sending/receiving, and message persistence.
    """
    
    async def connect(self):
        """
        Handle new WebSocket connection.
        Sets up the chat room and adds the channel to the room's group.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Removes the channel from the room's group.
        
        Args:
            close_code: The code indicating why the socket is being closed
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,

        )  

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.
        Processes the message and broadcasts it to the room if valid.
        
        Args:
            text_data (str): JSON string containing message data with keys:
                - message: The chat message content
                - username: The sender's username
                - room: The chat room identifier
        """
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        if message.strip():  # Check if message is not just whitespace
            # Send unencrypted message to channel layer
            await self.channel_layer.group_send(
                self.room_group_name,{
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'room': room,
                }
            )
            # Save encrypted message
            await self.save_message(username, room, message)
        else:
            # Send error message back to sender
            await self.send(text_data=json.dumps({
                'error': 'Message cannot be empty'
            }))

    async def chat_message(self, event):
        """
        Handle chat messages received from the channel layer.
        Broadcasts the message to all connected clients in the room.
        
        Args:
            event (dict): Contains message data with keys:
                - message: The chat message content
                - username: The sender's username
                - room: The chat room identifier
        """
        message = event['message']
        username = event['username']
        room = event['room']
        
        # For real-time messages, we don't need to decrypt since they haven't been encrypted yet
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        """
        Save the chat message to the database.
        The message will be encrypted before storage.
        
        Args:
            username (str): The sender's username
            room (str): The chat room identifier
            message (str): The message content to be saved
        """
        user = User.objects.get(username=username)
        room = ChatRoom.objects.get(slug=room)
        
        # Message will be encrypted in the model's save method
        ChatMessage.objects.create(
            user=user, 
            room=room, 
            message_content=message
        )
