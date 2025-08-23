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


# Allow only hardcoded hosts and append container's private IP
from socket import gethostbyname, gethostname

# Set your allowed hosts here
ALLOWED_HOSTS = [
    'yourdomain.com',
    'anotherdomain.com',
]

# Append the container's private IP address for ECS health checks
try:
    container_ip = gethostbyname(gethostname())
    if container_ip not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(container_ip)
    print(f"Appended container IP {container_ip} to ALLOWED_HOSTS.")
except Exception as e:
    print(f"Could not append container IP to ALLOWED_HOSTS: {e}")

print(f"ALLOWED_HOSTS at startup: {ALLOWED_HOSTS}")

# Patch Django's DisallowedHost exception to log the host being checked
import django.core.exceptions
_orig_disallowed_host = django.core.exceptions.DisallowedHost
class LoggedDisallowedHost(_orig_disallowed_host):
    def __init__(self, msg, *args, **kwargs):
        logger.error(f"DisallowedHost check failed: {msg} | ALLOWED_HOSTS: {ALLOWED_HOSTS}")
        super().__init__(msg, *args, **kwargs)
django.core.exceptions.DisallowedHost = LoggedDisallowedHost
