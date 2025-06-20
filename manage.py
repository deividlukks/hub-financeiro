#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
HUB Financeiro - Sistema de Gestão Financeira Integrada
"""

import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Adicionar comandos customizados
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        # Comando para inicializar o sistema
        if command == 'initialize':
            initialize_system()
            return
            
        # Comando para executar worker do Celery
        elif command == 'celery_worker':
            run_celery_worker()
            return
            
        # Comando para executar beat do Celery
        elif command == 'celery_beat':
            run_celery_beat()
            return
            
        # Comando para setup completo
        elif command == 'setup':
            setup_project()
            return
    
    execute_from_command_line(sys.argv)

def initialize_system():
    """Inicializa o sistema com dados básicos"""
    print("🚀 Inicializando HUB Financeiro...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')
    
    import django
    django.setup()
    
    from django.core.management import call_command
    
    try:
        # Executar migrações
        print("📊 Aplicando migrações...")
        call_command('migrate')
        
        # Carregar dados iniciais
        print("📈 Carregando dados iniciais...")
        call_command('loaddata', 'shared/fixtures/categories.json')
        call_command('loaddata', 'shared/fixtures/investor_profiles.json')
        call_command('loaddata', 'shared/fixtures/trading_pairs.json')
        
        # Criar superusuário se não existir
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Criando superusuário...")
            call_command('createsuperuser', '--noinput', 
                        username='admin', 
                        email='admin@hubfinanceiro.com')
        
        print("✅ Sistema inicializado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")

def run_celery_worker():
    """Executa o worker do Celery"""
    print("🔄 Iniciando Celery Worker...")
    
    import subprocess
    subprocess.call([
        'celery', '-A', 'hub_financeiro', 'worker', 
        '--loglevel=info', '--concurrency=4'
    ])

def run_celery_beat():
    """Executa o beat scheduler do Celery"""
    print("⏰ Iniciando Celery Beat...")
    
    import subprocess
    subprocess.call([
        'celery', '-A', 'hub_financeiro', 'beat', 
        '--loglevel=info', '--scheduler=django_celery_beat.schedulers:DatabaseScheduler'
    ])

def setup_project():
    """Setup completo do projeto"""
    print("🛠️ Configurando HUB Financeiro...")
    
    # Verificar dependências
    check_dependencies()
    
    # Criar diretórios necessários
    create_directories()
    
    # Configurar banco de dados
    setup_database()
    
    # Inicializar sistema
    initialize_system()
    
    print("🎉 Setup concluído! Execute 'python manage.py runserver' para iniciar.")

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'django', 'djangorestframework', 'celery', 'channels',
        'psycopg2-binary', 'redis', 'requests', 'pandas',
        'numpy', 'scikit-learn', 'yfinance', 'python-telegram-bot'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ Todas as dependências estão instaladas")

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    directories = [
        'logs',
        'media/uploads',
        'media/exports',
        'media/reports',
        'staticfiles',
        'shared/backups',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados")

def setup_database():
    """Configura o banco de dados"""
    print("🗄️ Configurando banco de dados...")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')
    
    import django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    
    try:
        # Testar conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        print("✅ Conexão com banco de dados estabelecida")
        
        # Executar migrações
        call_command('makemigrations')
        call_command('migrate')
        
        print("✅ Banco de dados configurado")
        
    except Exception as e:
        print(f"❌ Erro na configuração do banco: {e}")
        print("Verifique as configurações de banco no .env")
        sys.exit(1)

if __name__ == '__main__':
    main()