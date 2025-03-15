from flask_restful import Resource, reqparse
from app import db
from app.models import Customer

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

class CustomerListResource(Resource):
    def get(self):
        customers = Customer.query.all()
        return [{'id': customer.id, 'name': customer.name, 'email': customer.email} for customer in customers]

    def post(self):
        args = parser.parse_args()
        customer = Customer(name=args['name'], email=args['email'], password=args['password'])
        db.session.add(customer)
        db.session.commit()
        return {'id': customer.id, 'name': customer.name, 'email': customer.email}, 201

class CustomerResource(Resource):
    def get(self, id):
        customer = Customer.query.get_or_404(id)
        return {'id': customer.id, 'name': customer.name, 'email': customer.email}

    def put(self, id):
        args = parser.parse_args()
        customer = Customer.query.get_or_404(id)
        customer.name = args['name']
        customer.email = args['email']
        customer.password = args['password']
        db.session.commit()
        return {'id': customer.id, 'name': customer.name, 'email': customer.email}

    def delete(self, id):
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return '', 204
