from flask_restful import Resource, reqparse
from app import db
from app.models import Order

parser = reqparse.RequestParser()
parser.add_argument('customer_id', type=int, required=True, help='Customer ID cannot be blank')
parser.add_argument('status', type=str, required=True, help='Status cannot be blank')

class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [{'id': order.id, 'customer_id': order.customer_id, 'status': order.status} for order in orders]

    def post(self):
        args = parser.parse_args()
        order = Order(customer_id=args['customer_id'], status=args['status'])
        db.session.add(order)
        db.session.commit()
        return {'id': order.id, 'customer_id': order.customer_id, 'status': order.status}, 201

class OrderResource(Resource):
    def get(self, id):
        order = Order.query.get_or_404(id)
        return {'id': order.id, 'customer_id': order.customer_id, 'status': order.status}

    def put(self, id):
        args = parser.parse_args()
        order = Order.query.get_or_404(id)
        order.status = args['status']
        db.session.commit()
        return {'id': order.id, 'customer_id': order.customer_id, 'status': order.status}

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204
