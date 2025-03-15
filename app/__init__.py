from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import Config

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)

    from app.resources.product import ProductResource, ProductListResource
    from app.resources.customer import CustomerResource, CustomerListResource
    from app.resources.order import OrderResource, OrderListResource

    api.add_resource(ProductListResource, '/products')
    api.add_resource(ProductResource, '/products/<int:id>')
    api.add_resource(CustomerListResource, '/customers')
    api.add_resource(CustomerResource, '/customers/<int:id>')
    api.add_resource(OrderListResource, '/orders')
    api.add_resource(OrderResource, '/orders/<int:id>')

    return app
