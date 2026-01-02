"""
WSGI config for goexplorer project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goexplorer.settings')

application = get_wsgi_application()
