# import all routes admin
from src.routes.admin.auth_admin import auth_admin_bp
from src.routes.admin.user_admin import user_admin_bp
from src.routes.admin.messages_admin import messages_admin_bp
from src.routes.admin.request_admin import request_admin_bp
from src.routes.admin.dash_board_admin import dashboard_admin_bp
from src.routes.admin.notification_admin import notification_admin_bp


# Prefix for all routes admin
auth_admin_bp.url_prefix = "/api/admin/auth"
user_admin_bp.url_prefix = "/api/admin/user"
messages_admin_bp.url_prefix = "/api/admin/messages"
request_admin_bp.url_prefix = "/api/admin/request"
dashboard_admin_bp.url_prefix = "/api/admin/dashboard"
notification_admin_bp.url_prefix = "/api/admin/notification"


# import all routes client
from src.routes.client.auth_client import auth_client_bp
from src.routes.client.request_client import request_client_bp

# Prefix for all routes client
auth_client_bp.url_prefix = "/api/client/auth"
request_client_bp.url_prefix = "/api/client/request"


blueprints = [
    auth_admin_bp,
    user_admin_bp,
    messages_admin_bp,
    request_admin_bp,
    dashboard_admin_bp,
    notification_admin_bp,
    auth_client_bp,
    request_client_bp,
]
