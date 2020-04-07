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


@api.route('/product')
class Product(Resource):


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

    # Todo: add a get method to get a single product by product_id


@api.route('/getproduct')
class GetProduct(Resource):

    @api.expect(product_models.get_product_model)
    def post(self):
        data = api.payload
        response = DbOps.get_product('', data['pkey'])
        if response['success']:
            return response['product_object'], 200
        else:
            return response['message'], 500


@api.route('/check_stock')
class CheckStock(Resource):

    @api.expect(product_models.check_stock_model)
    def post(self):
        data = api.payload
        response = DbOps.check_stock('', data['basket_id'])
        if response['success']:
            return response['in_stock'], 200
        else:
            return response['message'], 500

@api.route('/all_products')
class AllProducts(Resource):


    def get(self):
        """
        Returns a list of all of the products
        """
        response = DbOps.get_all_products('')
        if response['success']:
            return response['products'], 200
        else:
            return response['message'], 500
