"""
ASGI config for HUB Financeiro
Configuração para suporte a WebSockets e comunicação em tempo real
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Configurar Django antes de importar models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')
django.setup()

# Importar routing após setup do Django
from platforms.web.api.websocket import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP requests
    "http": get_asgi_application(),
    
    # WebSocket connections
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})