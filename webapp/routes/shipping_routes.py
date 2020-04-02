import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import shipping_models
from webapp.util.db_operations import DbOps

@api.route('/update_shipping')
class UpdateShipping(Resource):


    @api.expect(shipping_models.update_shipping_model)
    def post(self):
        """
        Update the shipping info on an order
        """
        data = api.payload
        response = DbOps.update_order_status('', data['basket_id'], data['date'], data['shipper'], data['shipnum'])

        if response['changed']:
            return response['shipped'], 200
        else:
            return response['message'], 500
