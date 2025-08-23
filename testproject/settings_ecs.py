# Django settings for ECS
import os
from pathlib import Path

import logging
logger = logging.getLogger('django.allowed_hosts')

from .settings import *  # Import all default settings

# Override database settings for ECS if environment variables are set
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Allow hosts from env or default to all for ECS
_allowed_hosts_env = os.getenv('DJANGO_ALLOWED_HOSTS', '*')
if _allowed_hosts_env.strip() == '*':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_env.split(',') if h.strip()]

logger.info(f"ALLOWED_HOSTS at startup: {ALLOWED_HOSTS}")

# Patch Django's DisallowedHost exception to log the host being checked
import django.core.exceptions
_orig_disallowed_host = django.core.exceptions.DisallowedHost
class LoggedDisallowedHost(_orig_disallowed_host):
    def __init__(self, msg, *args, **kwargs):
        logger.error(f"DisallowedHost check failed: {msg} | ALLOWED_HOSTS: {ALLOWED_HOSTS}")
        super().__init__(msg, *args, **kwargs)
django.core.exceptions.DisallowedHost = LoggedDisallowedHost
