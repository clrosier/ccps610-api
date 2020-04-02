import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import sale_models
from webapp.util.db_operations import DbOps

@api.route('/check_sale')
class CheckSale(Resource):


    @api.expect(sale_models.check_sale)
    def post(self):
        """
        Checks if an item is on sale
        """
        data = api.payload
        response = DbOps.check_sale('', data['date'], data['product_id'])
        if response['changed']:
            return { "msg": response['message'], "on_sale": response['on_sale']}, 200
        else:
            return response['message'], 500
