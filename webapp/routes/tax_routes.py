import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import tax_models
from webapp.util.db_operations import DbOps

@api.route('/calculate_tax')
class CalculateTax(Resource):


    @api.expect(tax_models.tax_model)
    def post(self):
        """
        Calculate tax
        """
        data = api.payload
        response = DbOps.calculate_tax('', data['state'], data['subtotal'])

        if response['changed']:
            return response['tax_amount'], 200
        else:
            print(response['message'])
            return response['message'], 500
