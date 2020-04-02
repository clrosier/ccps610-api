from webapp import api
from flask_restplus import Resource, fields

login_model = api.model('Login', {
                            'username': fields.String(required=True, description='username identifier'),
                            'password': fields.String(required=True, description='password')})