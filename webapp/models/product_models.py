from webapp import api
from flask_restplus import Resource, fields

edit_product_model = api.model('Edit Product', {
                            'pkey': fields.String(required=True, description='The product key'),
                            'new_desc': fields.String(required=True, description='New description')})

add_product_model = api.model('Add Product', {
                            'product_name': fields.String(required=True, description='The product name'),
                            'product_desc': fields.String(required=True, description='New description'),
                            'product_img_file': fields.String(required=True, description='Name of the image file for the product'),
                            'product_price': fields.Float(required=True, description='The price of the new product'),
                            'product_status': fields.Integer(required=True, description='The active status for the new product (1 if active, 0 if inactive)')})