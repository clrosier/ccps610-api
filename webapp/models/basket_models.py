from webapp import api
from flask_restplus import Resource, fields

add_to_basket = api.model('Add To Basket', {
                            'basket_id': fields.Integer(required=True, description='The id of the order'),
                            'product_id': fields.Integer(required=True, description='The id of the product'),
                            'price': fields.Float(required=True, description='The price of the item'),
                            'quantity': fields.Integer(required=True, description='The amount of the product'),
                            'size_code': fields.Integer(required=True, description='The size code option'),
                            'form_code': fields.Integer(required=True, description='The form code option')})