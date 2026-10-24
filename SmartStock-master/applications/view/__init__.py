from applications.view.system import register_system_bps
from applications.view.plugin import register_plugin_views
from applications.view.member import register_member_bps
from applications.view.api import register_api_bps
from applications.view.stock import register_stock_bps
from applications.view.strategy import register_strategy_bps
from applications.view.trading import register_trading_bps
from applications.view.quantify import register_quantify_bps

def init_bps(app):
    register_system_bps(app)
    register_plugin_views(app)
    register_member_bps(app)
    register_api_bps(app)
    register_stock_bps(app)
    register_strategy_bps(app)
    register_trading_bps(app)
    register_quantify_bps(app)
