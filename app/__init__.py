from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    
    # Add a basic route for testing
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to ShopEase API!"})
    
    # Create a new Api instance tied to this specific app instance
    api = Api(app)
    
    # Register API resources
    from app.resources.product import ProductResource, ProductListResource
    from app.resources.customer import CustomerResource, CustomerListResource
    from app.resources.order import OrderResource, OrderListResource
    
    api.add_resource(ProductListResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(CustomerListResource, '/customers')
    api.add_resource(CustomerResource, '/customers/<int:id>')
    api.add_resource(OrderListResource, '/orders')
    api.add_resource(OrderResource, '/orders/<int:id>')
    
    # Add a debug route to list all registered endpoints
    @app.route('/debug/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'path': str(rule)
            })
        return jsonify(routes)

    return app
