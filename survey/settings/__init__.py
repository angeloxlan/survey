import os
from dotenv import load_dotenv


load_dotenv()

# Base settings
from .base import *

# Development settings
if os.environ.get('DJANGO_ENVIRONMENT') == 'development':
    from .development import *

# Production settings
elif os.environ.get('DJANGO_ENVIRONMENT') == 'production':
    from .production import *
