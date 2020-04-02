import cx_Oracle
from config import Config

class DbOps:

    def connect(self):
        """
        Connect to the oracle database using username and password

        :param: usr (str): The username to login
        :param: pwd (str): The password to login

        :returns: cursor (Oracle Cursor Object): If login was successful
        :returns: False (bool): If login was unsuccessful
        """
        try:
            # Get connection information from config.py
            usr = Config.ORACLE_USER
            pwd = Config.ORACLE_PASS
            host = Config.ORACLE_HOST
            port = Config.ORACLE_PORT
            sid  = Config.ORACLE_SID

            # Form the connection string and connect to the database
            conn = cx_Oracle.connect("%s/%s@%s:%s/%s"
                                    % (usr,pwd,host,port,sid))

            cursor = conn.cursor()
            return cursor
        except cx_Oracle.DatabaseError as e:
            print('Something went wrong.  Check it out: \n %s' % e)
            return False


    def edit_product_description(self, pkey, new_desc):
        """
        Edits the description of a product given it's product key and the new description

        :param: pkey (str): The product's identifier in the table
        :param: new_desc (str): The new description to replace the old one with

        :returns: response_object (dict): An object containing a dictionary with the products attributes / an error message as well as a 'changed' (bool) status
        """
        from webapp import cursor

        # Table name within the database
        __tablename__ = "BB_PRODUCT"

        try:
            # Call the UPDATE_DESCRIPTION stored procedure
            out_pkey, out_desc = cursor.callproc("UPDATE_DESCRIPTION",
                                    [pkey, new_desc])

            # Form an SQL query to get a description of the item we've updated and execute the SQL query
            sql = "SELECT PRODUCTNAME FROM %s WHERE IDPRODUCT = %s" % (__tablename__, pkey)
            product_name = cursor.execute(sql).fetchone()

            # Form a dict/JSON object to return to the user
            product_object = {
                "product_key": out_pkey,
                "product_name": product_name[0],
                "product_new_desc": out_desc
            }

            response_object = {
                "product_object": product_object,
                "changed": True
            }

            return response_object

        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "changed": False
            }

            return response_object


    def add_new_product(self, pname, pdesc, pimg, pprice, pactive):
        """
        Adds a new product and stores it in the database

        :param: pname (str): The name of the product
        :param: pdesc (str): The description of the new product
        :param: pimg (str): The name of the image file for the new product
        :param: pprice (float): The price of the new product
        :param: pactive (int): The active status of the new product (1 if active, 0 if inactive)
        """
        from webapp import cursor

        # Table name within the database
        __tablename__ = "BB_PRODUCT"

        try:
            output = cursor.callproc("PROD_ADD_SP",
                                    [pname, pdesc, pimg, pprice, pactive])
            print(output)
            # Form an SQL query to get a description of the item we've updated and execute the SQL query
            sql = "SELECT * FROM %s WHERE PRODUCTNAME='%s'" % (__tablename__, pname)
            print(sql)
            product_name = cursor.execute(sql).fetchone()

            # Form a dict/JSON object to return to the user
            product_object = {
                "product_name": product_name[0],
                "product_desc": product_name[1],
                "product_img_file": product_name[2],
                "product_price": product_name[3],
                "product_status": product_name[4]
            }

            response_object = {
                "product_object": product_object,
                "changed": True
            }

            return response_object
        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "changed": False
            }

            return response_object
