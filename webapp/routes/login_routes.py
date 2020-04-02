import cx_Oracle

from webapp import api
from flask_restplus import Resource, fields

from webapp.models import login_models

ns_usermgmt = api.namespace('user management', description='Management of user login and registration operations')

@api.route('/login')
class Login(Resource):


    @api.expect(login_models.login_model)
    def post(self):
        """
        Login to service
        """
        pass