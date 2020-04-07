from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from flask_cors import CORS

from webapp.util.db_operations import DbOps


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

cursor = DbOps.connect('')

from webapp.routes.login_routes import *
from webapp.routes.product_routes import *
from webapp.routes.tax_routes import *
from webapp.routes.shipping_routes import *
from webapp.routes.basket_routes import *
from webapp.routes.sale_routes import *

if __name__=="__main__":
    app.run()
