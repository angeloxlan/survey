import os
from dotenv import load_dotenv
from .base import *


load_dotenv()

# Development settings
if os.environ.get('DJANGO_ENVIRONMENT') == 'development':
    from .development import *

# Production settings
elif os.environ.get('DJANGO_ENVIRONMENT') == 'production':
    from .production import *
