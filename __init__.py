"""
HUB Financeiro - Sistema de Gestão Financeira Integrada

Sistema completo para gestão de finanças pessoais, investimentos e trading
com suporte a múltiplas plataformas (Web, Telegram, Mobile, WhatsApp)

Funcionalidades principais:
- Gestão de Finanças Pessoais
- Gestão de Investimentos com IA
- Trading com análise técnica e fundamentalista
- Chatbot inteligente
- Notificações em tempo real
- Análises e relatórios avançados

Desenvolvido com Django, Vue.js, React Native e integração com APIs financeiras
"""

__version__ = '1.0.0'
__author__ = 'Equipe HUB Financeiro'
__email__ = 'contato@hubfinanceiro.com'

# Configuração do Celery
from .celery import app as celery_app

__all__ = ('celery_app',)

# Banner de inicialização
def print_banner():
    """Exibe banner do sistema na inicialização"""
    banner = """
    ██╗  ██╗██╗   ██╗██████╗     ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██╗██████╗  ██████╗ 
    ██║  ██║██║   ██║██╔══██╗    ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██║██╔══██╗██╔═══██╗
    ███████║██║   ██║██████╔╝    █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  ██║██████╔╝██║   ██║
    ██╔══██║██║   ██║██╔══██╗    ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  ██║██╔══██╗██║   ██║
    ██║  ██║╚██████╔╝██████╔╝    ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗██║██║  ██║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝╚═╝  ╚═╝ ╚═════╝ 
    
    Sistema de Gestão Financeira Integrada v{version}
    🚀 Plataforma completa para controle financeiro pessoal e investimentos
    """.format(version=__version__)
    
    print(banner)

# Verificação de dependências críticas na inicialização
def check_critical_dependencies():
    """Verifica dependências críticas do sistema"""
    import sys
    
    critical_deps = {
        'django': 'Django framework',
        'rest_framework': 'Django REST Framework', 
        'celery': 'Celery para tarefas assíncronas',
        'channels': 'Django Channels para WebSockets',
        'redis': 'Redis para cache e message broker'
    }
    
    missing_deps = []
    
    for dep, description in critical_deps.items():
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(f"{dep} ({description})")
    
    if missing_deps:
        print("❌ Dependências críticas faltando:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nExecute: pip install -r requirements.txt")
        sys.exit(1)

# Configurações de inicialização
import os
if os.environ.get('DJANGO_SETTINGS_MODULE'):
    try:
        import django
        from django.conf import settings
        
        # Verificar se Django está configurado
        if not settings.configured:
            django.setup()
            
        # Executar verificações apenas em desenvolvimento
        if settings.DEBUG:
            check_critical_dependencies()
            
    except Exception as e:
        print(f"⚠️ Aviso na inicialização: {e}")

# Metadata do sistema
SYSTEM_INFO = {
    'name': 'HUB Financeiro',
    'version': __version__,
    'description': 'Sistema de Gestão Financeira Integrada',
    'platforms': ['Web', 'Telegram', 'Mobile', 'WhatsApp'],
    'features': [
        'Gestão de Finanças Pessoais',
        'Portfolio de Investimentos',
        'Trading com IA',
        'Análise Fundamentalista',
        'Chatbot Inteligente',
        'Notificações em Tempo Real',
        'Relatórios Avançados'
    ],
    'technologies': [
        'Django', 'Vue.js', 'React Native', 'Celery',
        'Redis', 'PostgreSQL', 'WebSockets', 'REST API'
    ]
}

def get_system_info():
    """Retorna informações do sistema"""
    return SYSTEM_INFO