import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import basket_models
from webapp.util.db_operations import DbOps


@api.route('/add_to_basket')
class AddToBasket(Resource):


    @api.expect(basket_models.add_to_basket)
    def post(self):
        """
        Add item to the basket
        """
        data = api.payload
        response = DbOps.add_item_to_basket('', data['basket_id'], data['product_id'], data['price'], data['quantity'], data['size_code'], data['form_code'])
        if response['changed']:
            return response['message'], 200
        else:
            return response['message'], 500
