"""
URL Configuration for HUB Financeiro
Sistema completo de gestão financeira
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Importar ViewSets das APIs
from platforms.web.api.auth import AuthViewSet
from platforms.web.api.portfolio import PortfolioViewSet
from platforms.web.api.trading import TradingViewSet
from platforms.web.api.market_data import MarketDataViewSet
from platforms.web.api.news import NewsViewSet
from platforms.web.api.dividends import DividendViewSet
from platforms.web.api.signals import SignalViewSet
from platforms.web.api.ai_chat import AIChatViewSet
from platforms.web.api.chatbot import ChatbotViewSet
from platforms.web.api.analysis import AnalysisViewSet
from platforms.web.api.insights import InsightsViewSet
from platforms.web.api.forex import ForexViewSet
from platforms.web.api.daytrading import DayTradingViewSet
from platforms.web.api.investments import InvestmentViewSet
from platforms.web.api.transactions import TransactionViewSet
from platforms.web.api.reports import ReportViewSet
from platforms.web.api.export import ExportViewSet

# Configuração do Router da API
router = DefaultRouter()

# Registro das APIs
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'trading', TradingViewSet, basename='trading')
router.register(r'market-data', MarketDataViewSet, basename='market-data')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'dividends', DividendViewSet, basename='dividends')
router.register(r'signals', SignalViewSet, basename='signals')
router.register(r'ai-chat', AIChatViewSet, basename='ai-chat')
router.register(r'chatbot', ChatbotViewSet, basename='chatbot')
router.register(r'analysis', AnalysisViewSet, basename='analysis')
router.register(r'insights', InsightsViewSet, basename='insights')
router.register(r'forex', ForexViewSet, basename='forex')
router.register(r'daytrading', DayTradingViewSet, basename='daytrading')
router.register(r'investments', InvestmentViewSet, basename='investments')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'export', ExportViewSet, basename='export')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Platform URLs
    path('web/', include('platforms.web.urls')),
    path('telegram/', include('platforms.telegram.urls')),
    path('mobile/', include('platforms.mobile.urls')),
    path('whatsapp/', include('platforms.whatsapp.urls')),
    
    # WebSocket URLs
    path('ws/', include('platforms.web.api.websocket')),
    
    # Redirect root to web platform
    path('', RedirectView.as_view(url='/web/', permanent=False)),
    
    # Health check
    path('health/', include('core.health_urls')),
]

# URLs específicas para desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar (se instalado)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Customização do Admin
admin.site.site_header = "HUB Financeiro - Administração"
admin.site.site_title = "HUB Financeiro Admin"
admin.site.index_title = "Painel Administrativo"

# Handler para erros personalizados
handler404 = 'platforms.web.views.custom_404_view'
handler500 = 'platforms.web.views.custom_500_view'