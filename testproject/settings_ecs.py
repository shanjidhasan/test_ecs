# Logging configuration to ensure allowed_hosts logger outputs to console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.allowed_hosts': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
# Django settings for ECS
import os
from pathlib import Path

import logging
import re
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
    # Allow all hostnames and all IPv4 addresses with optional port
    ALLOWED_HOSTS = ['*', re.compile(r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$')]
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
