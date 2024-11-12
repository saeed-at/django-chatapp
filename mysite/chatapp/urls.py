from django.urls import path
from . import views

"""URL configuration for the chat application.
Defines the URL patterns and their corresponding view functions.
"""

urlpatterns = [
    # Landing/welcome page
    path('', views.welcome, name='welcome-url'),
    
    # List of all chat rooms
    path('rooms/', views.index, name='index-url'),
    
    # Search functionality for rooms/users
    path('search/', views.search_view, name='search-url'),
    
    # Individual chatroom view, accessed by room slug
    path('rooms/<slug:slug>/', views.chatroom, name='chatroom-url'),
    
    # User logout endpoint
    path("logout/", views.logout_view, name='logout-url'),
    
    # About page with application information
    path('about/', views.about_view, name='about-url'),

]