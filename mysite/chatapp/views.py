from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from cryptography.fernet import Fernet
from django.conf import settings
import os
from django.http import HttpResponse

def welcome(request):
    """
    Display welcome page for unauthenticated users.
    Redirects authenticated users to the index page.
    """
    if request.user.is_authenticated:
        return redirect('index-url')
    return render(request, 'chatapp/welcome.html')

@login_required(login_url='welcome-url')
def index(request):
    """
    Display the main index page showing all available chatrooms.
    Requires user authentication.
    """
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html', {'chatrooms': chatrooms})

@login_required(login_url='welcome-url')
def chatroom(request, slug):
    """
    Display a specific chatroom and its messages.
    
    Args:
        request: HTTP request object
        slug: Unique identifier for the chatroom
        
    Returns:
        Rendered chatroom page with messages and user list
    """
    chatroom = ChatRoom.objects.get(slug=slug)
    # Limit to latest 2000 messages for performance
    messages = ChatMessage.objects.filter(room=chatroom)[0:2000]
    
    # Get distinct users with their full user objects
    users_in_chat = list(get_user_model().objects.filter(
        id__in=ChatMessage.objects.filter(room=chatroom).values_list('user', flat=True).distinct()
    ))
    # Add current user to the users list if not already present
    if request.user not in users_in_chat:
        users_in_chat.append(request.user)
    return render(request, 'chatapp/room.html', {
        'chatroom': chatroom, 
        'messages': messages,
        'users_in_chat': users_in_chat
    })

@login_required(login_url='welcome-url')
def search_view(request):
    """
    Search for chatrooms based on name.
    Returns filtered results matching the search query.
    """
    query = request.GET.get('q', '')   
    results = ChatRoom.objects.filter(name__icontains=query)
    return render(request, 'chatapp/results.html', {"results": results, 'query': query})

def logout_view(request):
    """
    Log out the current user and redirect to welcome page.
    """
    logout(request)
    return redirect('welcome-url')

def check_encryption(request):
    """
    Debug endpoint to verify message encryption.
    Attempts to decrypt the latest message and returns encryption status.
    
    Returns:
        JsonResponse containing original message, decrypted message,
        and encryption status or error message if decryption fails.
    """
    # Get the last message from database
    last_message = ChatMessage.objects.last()
    if last_message:
        try:
            # Try to decrypt the message using the app's encryption key
            f = Fernet(settings.ENCRYPTION_KEY)
            decrypted = f.decrypt(last_message.message_content.encode()).decode()
            
            return JsonResponse({
                'original_stored': last_message.message_content,
                'decrypted': decrypted,
                'is_encrypted': last_message.message_content != decrypted
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'stored_message': last_message.message_content
            })
    return JsonResponse({'error': 'No messages found'})

def about_view(request):
    """
    Display the about page of the application.
    """
    return render(request, 'chatapp/about.html')

