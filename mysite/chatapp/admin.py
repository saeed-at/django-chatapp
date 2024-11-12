from django.contrib import admin
from .models import ChatRoom, ChatMessage

# Register models to make them accessible in Django's admin interface
# This allows administrators to view, create, edit, and delete records
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)