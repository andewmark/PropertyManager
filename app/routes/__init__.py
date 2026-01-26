from .property_routes import property_bp
from .building_routes import building_bp
from .main_routes import main


def register_routes(app):
    app.register_blueprint(property_bp)
    app.register_blueprint(building_bp)
    app.register_blueprint(main)
