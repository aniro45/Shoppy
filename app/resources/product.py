from flask_restful import Resource, reqparse
from app import db
from app.models import Product

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('price', type=float, required=True, help='Price cannot be blank')
parser.add_argument('description', type=str)

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return [{'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description} for product in products]

    def post(self):
        args = parser.parse_args()
        product = Product(name=args['name'], price=args['price'], description=args.get('description'))
        db.session.add(product)
        db.session.commit()
        return {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}, 201

class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}

    def put(self, id):
        args = parser.parse_args()
        product = Product.query.get_or_404(id)
        product.name = args['name']
        product.price = args['price']
        product.description = args.get('description')
        db.session.commit()
        return {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204
