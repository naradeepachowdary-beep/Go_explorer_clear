"""
ASGI config for goexplorer project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goexplorer.settings')

application = get_asgi_application()
