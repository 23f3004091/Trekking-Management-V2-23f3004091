from .admin_routes import admin_bp
from .auth_routes import auth_bp
from .staff_routes import staff_bp
from .trekker_routes import trekker_bp

__all__ = ['admin_bp', 'auth_bp', 'staff_bp', 'trekker_bp']