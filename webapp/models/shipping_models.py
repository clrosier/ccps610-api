from webapp import api
from flask_restplus import Resource, fields

update_shipping_model = api.model('Update Shipping Info', {
                            'basket_id': fields.Integer(required=True, description='The id of the order'),
                            'date': fields.Date(required=True, description='The date (DD-MMM-YY ex. 24-JAN-12)'),
                            'shipper': fields.String(required=True, description='The company who is shipping the order'),
                            'shipnum': fields.String(required=True, description='The shipping number')})