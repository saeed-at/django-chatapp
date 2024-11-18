# Django secret key used for cryptographic signing. Should be kept secret and changed in production
SECRET_KEY = 'django-insecure-vw7i@8gv+!*nujkmec+d7pn-_-ks=pmmfaxm6k&38d+ieptfkr'

# For development environment, set DEBUG to True
DEBUG = False

# List of host/domain names that this Django site can serve
# Empty list means only localhost is allowed
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.240.242']

# Custom encryption key used for additional data encryption
# This should also be kept secret and changed in production
ENCRYPTION_KEY = b'dQVQKXWkuzf4xr-jFzQQZUwRwGjXK_ZN3siGCNCVl5c='

