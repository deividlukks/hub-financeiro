"""
WSGI config for HUB Financeiro
Configuração para deployment em produção com servidores WSGI
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Adicionar o diretório do projeto ao Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurar variável de ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')

# Configurações para produção
if os.environ.get('DJANGO_ENV') == 'production':
    # Configurações específicas de produção
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings.production')

# Obter aplicação WSGI
application = get_wsgi_application()

# Middleware personalizado para produção
class SecurityHeadersMiddleware:
    """Middleware para adicionar headers de segurança"""
    
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def new_start_response(status, response_headers):
            # Adicionar headers de segurança
            security_headers = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', 'DENY'),
                ('X-XSS-Protection', '1; mode=block'),
                ('Referrer-Policy', 'strict-origin-when-cross-origin'),
                ('Permissions-Policy', 'geolocation=(), microphone=(), camera=()'),
            ]
            
            response_headers.extend(security_headers)
            return start_response(status, response_headers)
        
        return self.app(environ, new_start_response)

# Aplicar middleware de segurança em produção
if os.environ.get('DJANGO_ENV') == 'production':
    application = SecurityHeadersMiddleware(application)

# Configuração de logging para produção
if os.environ.get('DJANGO_ENV') == 'production':
    import logging
    
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler('/var/log/hub_financeiro/django.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("HUB Financeiro WSGI application initialized")