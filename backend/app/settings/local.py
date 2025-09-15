"""
Django settings for local development.

This file imports the base settings and overrides them with settings
suitable for a local development environment.
"""
from .base import *

# --- Development-specific settings ---

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts for local development convenience.
ALLOWED_HOSTS = ["*"]

# --- Optional Development Tools ---

# Add django-debug-toolbar if it's installed
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#
# # Required for debug_toolbar
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

# --- Email ---
# In development, we can print emails to the console instead of sending them.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- Logging ---
# You can add more verbose logging for development here if needed.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
