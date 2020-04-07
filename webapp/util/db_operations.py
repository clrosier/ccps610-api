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

        :param: pkey (int): The product's identifier in the table
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
            # Called stored proceduce PROD_ADD_SP to add a new product
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


    def calculate_tax(self, state, subtotal):

        """
        Calculates the tax given the state and the subtotal

        :param: state (str): The state from which the product is purchased
        :param: subtotal (float): The subtotal of the product purchase

        :returns: The tax amount for the purchase
        """
        from webapp import cursor

        # Table name within the database
        # __tablename__ = "BB_TAX"

        try:
            # Called stored proceduce PROD_ADD_SP to add a new product
            output = cursor.callproc("TAX_COST_SP",
                                    [state, subtotal, 0])

            response_object = {
                "tax_amount": "{:.2f}".format(output[2]),
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
        

    def update_order_status(self, basket_id, date, shipper, shipnum):
        """
        Updates the status of an order

        :param: basket_id (int): The state from which the product is purchased
        :param: date (date): The date that the order was shipped
        :param: shipper (str): The company that is shipping the order
        :param: shipnum (str): The tracking number of the shipment

        :returns: True (bool): if successfully updated order status
        :returns: False (bool): if unsuccessfully updated order status
        """
        from webapp import cursor

        try:
            output = cursor.callproc("STATUS_SHIP_SP",
                                    [basket_id, date, shipper, shipnum])

            shipping_info = {
                "basket_id": basket_id,
                "date": date,
                "shipper": shipper,
                "shipping_num": shipnum,
                "is_shipped": True
            }

            response_object = {
                "shipped": shipping_info,
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


    def add_item_to_basket(self, basket_id, product_id, price, quantity, size_code, form_code):
        """
        Adds an item to the user's basket

        :param: basket_id (int): The id of the user's basket
        :param: product_id (int): The id of the product
        :param: price (float): The price of the item
        :param: quantity (int): The amount of the product
        :param: size_code (int): The size code option
        :param: form_code (int): The form code option

        :returns: response_object (dict): An object containing a dictionary with the products attributes / an error message as well as a 'changed' (bool) status
        """
        from webapp import cursor

        try:
            output = cursor.callproc("BASKET_ADD_SP",
                                    [basket_id, product_id, price, quantity, size_code, form_code])

            response_object = {
                "message": "Successfully added item to basket.",
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


    def check_sale(self, date, product_id):
        """
        Adds an item to the user's basket

        :param: date (date): The date to check whether it's within the sale date
        :param: product_id (int): The id of the product

        :returns: response_object (dict): An object containing a dictionary with the products attributes / an error message as well as a 'changed' (bool) status
        """
        
        from webapp import cursor

        # Table name within the database
        # __tablename__ = "BB_BASKETITEM"

        try:
            output = cursor.callfunc("CK_SALE_SF", str,
                                    [date, product_id])

            on_sale = False
            if output == 'ON SALE!':
                on_sale = True

            response_object = {
                "message": output,
                "on_sale": on_sale,
                "changed": True
            }

            return response_object
        except cx_Oracle.DatabaseError as e:
            print('error')
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "changed": False
            }
            return response_object

    
    def get_all_products(self):

        from webapp import cursor
        # Table name within the database
        __tablename__ = "BB_PRODUCT"

        try:
            # Form an SQL query to get a description of the item we've updated and execute the SQL query
            sql = "SELECT * FROM %s ORDER BY IDPRODUCT" % __tablename__
            products = cursor.execute(sql).fetchall()
            product_list = []
            for product in products:
                pid = product[0]
                name = product[1]
                desc = product[2]
                img_loc = product[3]
                price = product[4]
                sale_price = product[7] if product[7] != None else None
                sale_start = str(product[5]) if product[7] != None else None
                sale_end = str(product[6]) if product[7] != None else None

                product_list.append({"pid": pid,
                                     "name": name,
                                     "desc": desc,
                                     "img_loc": img_loc,
                                     "price": price,
                                     "sale_price": sale_price,
                                     "sale_start": sale_start,
                                     "sale_end": sale_end
                                     })
            
            response_object = {
                "products": product_list,
                "success": True
            }

            return response_object

        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "success": False
            }

            return response_object


    def get_product(self, product_id):
        from webapp import cursor

        # Table name within the database
        __tablename__ = "BB_PRODUCT"

        try:
            # Form an SQL query to get a description of the item we've updated and execute the SQL query
            sql = "SELECT * FROM %s WHERE IDPRODUCT='%s'" % (__tablename__, product_id)
            product_name = cursor.execute(sql).fetchone()

            # Form a dict/JSON object to return to the user
            product_object = {
                "product_name": product_name[1],
                "product_desc": product_name[2],
                "product_img_file": product_name[3],
                "product_price": product_name[4]
            }

            response_object = {
                "product_object": product_object,
                "success": True
            }

            return response_object
        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "success": False
            }

            return response_object


    def check_stock(self, basket_id):
         
        from webapp import cursor

        try:
            output = cursor.callproc("STOCK_CHECK",
                                    [basket_id])

            print(output)

            response_object = {
                "in_stock": True,
                "success": True
            }

            return response_object
        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "success": False
            }

            return response_object


    def get_items_in_basket(self, basket_id):
         
        from webapp import cursor
        # Table name within the database
        __tablename__ = "BB_BASKETITEM"

        try:
            # Form an SQL query to get a description of the item we've updated and execute the SQL query
            sql = "SELECT * FROM %s WHERE IDBASKET=%s" % (__tablename__, basket_id)
            products = cursor.execute(sql).fetchall()
            product_list = []
            for product in products:
                pid = product[1]

                product_list.append(pid)
            
            response_object = {
                "products": product_list,
                "success": True
            }

            return response_object

        except cx_Oracle.DatabaseError as e:
            msg = 'Something went wrong.  Check it out: \n %s' % e
            response_object = {
                "message": msg,
                "success": False
            }

            return response_object
