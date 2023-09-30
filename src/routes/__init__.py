# import all routes admin
from src.routes.admin.auth_admin import auth_admin_bp

# import all routes client
from src.routes.client.auth_client import auth_client_bp

blueprints = [auth_admin_bp, auth_client_bp]
