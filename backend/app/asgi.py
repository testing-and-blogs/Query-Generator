"""
ASGI config for the NLQ backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# The DJANGO_SETTINGS_MODULE is expected to be set by the environment
# (e.g., by manage.py or the Gunicorn command).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')

# This is the default ASGI application.
application = get_asgi_application()

# If using Django Channels for WebSockets, the setup would look more like this:
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import some_app.routing
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             some_app.routing.websocket_urlpatterns
#         )
#     ),
# })
