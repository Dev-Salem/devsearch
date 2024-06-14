"""
WSGI config for devsearch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
print("WSGI module loaded", file=sys.stderr)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devsearch.settings')

application = get_wsgi_application()

print("Application loaded", file=sys.stderr)
