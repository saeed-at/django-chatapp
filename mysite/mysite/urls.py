# Import necessary Django modules
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Define URL patterns for the entire project
urlpatterns = [
    # Django admin interface URL
    path('admin/', admin.site.urls),
    
    # Root URL pattern - includes all URLs from chatapp.urls
    path('', include('chatapp.urls')),
    
    # Authentication URLs provided by django-allauth
    path("accounts/", include("allauth.urls")),

# Add support for serving media files during development
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
