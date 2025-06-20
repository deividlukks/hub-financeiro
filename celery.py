"""
Configuração do Celery para HUB Financeiro
Processamento de tarefas assíncronas para análises financeiras
"""

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub_financeiro.settings')

app = Celery('hub_financeiro')

# Usar configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tarefas automaticamente
app.autodiscover_tasks()

# Configuração de tarefas periódicas
app.conf.beat_schedule = {
    # Atualização de dados de mercado a cada 5 minutos
    'update-market-data': {
        'task': 'core.services.market_data_service.update_market_data',
        'schedule': crontab(minute='*/5'),
    },
    
    # Atualização de notícias a cada 15 minutos
    'update-financial-news': {
        'task': 'core.services.news_service.fetch_latest_news',
        'schedule': crontab(minute='*/15'),
    },
    
    # Análise de dividendos diariamente às 8h
    'analyze-dividends': {
        'task': 'core.services.dividend_service.analyze_upcoming_dividends',
        'schedule': crontab(hour=8, minute=0),
    },
    
    # Geração de sinais de trading a cada hora
    'generate-trading-signals': {
        'task': 'core.services.trading_signals_service.generate_signals',
        'schedule': crontab(minute=0),
    },
    
    # Análise fundamentalista diária às 9h
    'fundamental-analysis': {
        'task': 'core.services.fundamental_analysis_service.run_daily_analysis',
        'schedule': crontab(hour=9, minute=0),
    },
    
    # Atualização de dados forex a cada 30 minutos
    'update-forex-data': {
        'task': 'core.services.forex_service.update_forex_rates',
        'schedule': crontab(minute='*/30'),
    },
    
    # Geração de insights por IA diariamente às 7h
    'generate-ai-insights': {
        'task': 'core.services.ai_service.generate_daily_insights',
        'schedule': crontab(hour=7, minute=0),
    },
    
    # Verificação de alertas de risco a cada 10 minutos
    'risk-alerts': {
        'task': 'core.services.risk_profile_service.check_risk_alerts',
        'schedule': crontab(minute='*/10'),
    },
    
    # Backup dos dados diariamente às 2h
    'daily-backup': {
        'task': 'core.services.backup_service.create_daily_backup',
        'schedule': crontab(hour=2, minute=0),
    },
    
    # Limpeza de dados antigos semanalmente
    'cleanup-old-data': {
        'task': 'core.services.maintenance_service.cleanup_old_data',
        'schedule': crontab(hour=3, minute=0, day_of_week=1),
    },
    
    # Notificações de dividendos
    'dividend-notifications': {
        'task': 'core.services.notification_service.send_dividend_notifications',
        'schedule': crontab(hour=10, minute=0),
    },
    
    # Análise de performance de carteira diária às 18h
    'portfolio-performance': {
        'task': 'core.services.portfolio_service.calculate_daily_performance',
        'schedule': crontab(hour=18, minute=0),
    },
}

# Configurações adicionais
app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    
    # Configurações de roteamento de tarefas
    task_routes={
        'core.services.market_data_service.*': {'queue': 'market_data'},
        'core.services.trading_signals_service.*': {'queue': 'trading'},
        'core.services.ai_service.*': {'queue': 'ai_processing'},
        'core.services.notification_service.*': {'queue': 'notifications'},
    },
    
    # Configurações de worker
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # Configurações de resultado
    result_expires=3600,  # 1 hora
    
    # Configurações de retry
    task_default_retry_delay=60,  # 60 segundos
    task_max_retries=3,
)

@app.task(bind=True)
def debug_task(self):
    """Tarefa de debug para testar a configuração do Celery"""
    print(f'Request: {self.request!r}')
    return 'Debug task executed successfully'

# Tarefa para monitorar a saúde do sistema
@app.task
def health_check():
    """Verifica a saúde dos serviços críticos"""
    from core.services.health_service import HealthService
    
    health_service = HealthService()
    return health_service.run_health_check()

# Configuração de logging para Celery
app.conf.update(
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)