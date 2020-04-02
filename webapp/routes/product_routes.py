import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import product_models
from webapp.util.db_operations import DbOps


@api.route('/edit')
class EditProduct(Resource):


    @api.expect(product_models.edit_product_model)
    def post(self):
        """
        Edit the product description
        """
        data = api.payload
        response = DbOps.edit_product_description('', data['pkey'], data['new_desc'])
        if response['changed']:
            return response['product_object'], 200
        else:
            return response['message'], 500


@api.route('/add')
class AddProduct(Resource):


    @api.expect(product_models.add_product_model)
    def post(self):
        """
        Add a new product
        """
        data = api.payload
        response = DbOps.add_new_product('', data['product_name'], data['product_desc'], data['product_img_file'], data['product_price'], data['product_status'])
        if response['changed']:
            return response['product_object'], 200
        else:
            return response['message'], 500
