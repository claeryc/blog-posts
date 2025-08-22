"""
WSGI config for blogsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the Python path
project_home = '/home/claeryc/myblog/blog-posts'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()