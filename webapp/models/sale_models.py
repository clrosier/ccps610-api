from webapp import api
from flask_restplus import Resource, fields

check_sale = api.model('Check Sale', {
                            'date': fields.Date(required=True, description='date to check whether the it\'s in the sale period'),
                            'product_id': fields.Integer(required=True, description='The id of the product')})