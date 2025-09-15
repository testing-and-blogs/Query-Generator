"""
Django settings for production environments.

This file imports the base settings and overrides them with settings
suitable for a production deployment. It assumes that environment variables
are used to configure sensitive values.
"""
from .base import *

# --- Production-specific settings ---

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts should be set to the domain of the application
# It's recommended to load this from an environment variable.
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# --- Security Settings ---
# These settings are crucial for a secure production deployment.

# Enforce HTTPS. Nginx/reverse proxy should handle the redirect, but this is a fallback.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Use secure cookies for sessions and CSRF.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent the app from being loaded in an iframe to avoid clickjacking.
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# --- Database ---
# Ensure database connections are persistent to improve performance.
DATABASES['default']['CONN_MAX_AGE'] = 60 # 60 seconds

# --- Caching ---
# Use a more robust cache backend for production if needed, but Redis is a good default.
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.environ.get('REDIS_URL'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# --- Logging ---
# In production, logs should be structured (e.g., JSON) for easier processing.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'app': { # Logger for our own apps
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Add python-json-logger to pyproject.toml if using this logging config.
# poetry add python-json-logger
