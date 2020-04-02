from webapp import api
from flask_restplus import Resource, fields

tax_model = api.model('Tax Amount', {
                            'state': fields.String(required=True, description='The state from which the product was purchased'),
                            'subtotal': fields.Float(required=True, description='The amount of the purchase pre-tax')})
