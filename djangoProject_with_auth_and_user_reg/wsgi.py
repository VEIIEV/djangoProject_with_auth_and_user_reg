"""
WSGI config for djangoProject_with_auth_and_user_reg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject_with_auth_and_user_reg.settings')

application = get_wsgi_application()
