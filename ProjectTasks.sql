/* @author  Ramanpreet Hira 
---------------------
----Task 1 Procedure 
---------------------
This procedure is used to update Product Description using product Id as a parameter value */

CREATE OR REPLACE PROCEDURE UPDATE_DESCRIPTION (
  P_prod_id           BB_Product.idproduct%TYPE,
  P_description       BB_Product.description%TYPE)
  IS
BEGIN  
     UPDATE  BB_Product 
     SET    description = P_description 
     WHERE   idproduct  =  P_prod_id;
     DBMS_OUTPUT.PUT_LINE('Updated Product tabe  '|| SQL%ROWCOUNT || 'row ');
     COMMIT;
END;
/


-- Exceuting store Produce for testing purpose 
Begin
  UPDATE_DESCRIPTION(1,'CapressoBar Model#388');
END;
/

----------------------
--- Task 2 Procedure 
----------------------

CREATE OR REPLACE PROCEDURE PROD_ADD_SP(
     p_product_name   IN        BB_Product.productName%TYPE,
     p_description      IN       BB_Product.description%TYPE,
     p_product_image    IN      BB_Product.productImage%TYPE,
     p_price            IN      BB_Product.price%TYPE,
     p_active_status     IN     BB_Product.active%TYPE)
 
  IS 
BEGIN 
    INSERT INTO BB_PRODUCT (idproduct, productName, description , ProductImage, Price , Active)
    VALUES(bb_prodid_seq.nextval, p_product_name, p_description, p_product_image, p_price, p_active_status);
    COMMIT;

END;
/

-- Task2 Exceuting store Produce for testing purpose 
    
Begin
  PROD_ADD_SP('Roasted Blend', 'Well-balanced mix of roasted beans, a medium body','roasted.jpg',9.50,1);
END;
/


---TASK 2 SEARCH FUNCTION 
CREATE OR REPLACE FUNCTION SEARCH(
  p_productName   BB_Product.productName%TYPE)
  RETURN BB_PRODUCT%ROWTYPE    AS 
  v_row  BB_PRODUCT%ROWTYPE;
BEGIN 
  SELECT *
  INTO   v_row
  FROM   BB_PRODUCT
  WHERE  ProductName = p_productName;
  RETURN v_row;
END;
/
  
--  Execute task 2 function 
DECLARE
  v_row BB_PRODUCT%ROWTYPE;
BEGIN
  v_row := search( 'Brazil' );
  DBMS_OUTPUT.PUT_LINE(v_row.Description );
END;
/

----------------------------
------- Task 3  Procedure 
----------------------------
CREATE OR REPLACE PROCEDURE TAX_COST_SP(
    p_shopper_state   IN    bb_tax.State%TYPE,
    p_basket_subtotal   IN   NUMBER ,
    p_tax    OUT   NUMBER) 
IS 
   v_taxrate    BB_TAX.TAXRATE%TYPE;
BEGIN 
    SELECT taxrate INTO  v_taxrate
    FROM BB_TAX 
    WHERE state = p_shopper_state; 
    p_tax := p_basket_subtotal*v_taxrate;
END;
/
---- Exceute Task 3 Procedure 
DECLARE
  v_tax  NUMBER;
BEGIN
 TAX_COST_SP('VA',100,v_tax);
 DBMS_OUTPUT.PUT_LINE(v_tax );
END;
/

--------------------------------------
------ Task 4 Procedure ---------
--------------------------------------

CREATE OR REPLACE PROCEDURE STATUS_SHIP_SP(
        p_basket_id   IN  BB_BASKETSTATUS.IDBASKET%TYPE,
        p_date     IN  date ,
        p_shipper   IN  BB_BASKETSTATUS.SHIPPER%TYPE,
        p_shipnum   IN  BB_BASKETSTATUS.SHIPPINGNUM%TYPE)
  IS      
BEGIN  
   INSERT INTO BB_BASKETSTATUS( idstatus, idbasket, idstage, dtstage,shipper, shippingnum)
   VALUES ( bb_status_seq.NEXTVAL,P_basket_id,3, p_date,p_shipper,P_shipnum);
   COMMIT;
END;
/
 
----  EXECUTE TASK 4 PROCEDURE ---         
execute STATUS_SHIP_SP(3,'20-FEB-12','UPS','ZW2384YXK4957');        

------------------------------------
-------- TASK 5 PROCEDURE -------
---------------------------------
 CREATE OR REPLACE PROCEDURE BASKET_ADD_SP(
    p_basket_id    IN   BB_BASKETITEM.IDBASKET%TYPE,
    p_product_id   IN   BB_BASKETITEM.IDPRODUCT%TYPE,
    p_price        IN   BB_BASKETITEM.PRICE%TYPE,
    p_quantity     IN   BB_BASKETITEM.QUANTITY%TYPE,
    p_size_code    IN   NUMBER,
    p_form_code    IN   NUMBER)
  IS  
 BEGIN 
    INSERT INTO BB_BASKETITEM
    VALUES(BB_IDBASKETITEM_SEQ.NEXTVAL, p_product_id, p_price , p_quantity, p_basket_id, p_size_code, p_form_code);
    COMMIT;
 END;
 /
    
----  EXECUTE TASK 5 PROCEDURE ---         
execute BASKET_ADD_SP(14,8,10.80,1,2,4);      
 
---------------------------------------------
----- TASK 6 PROCEDURE -----------
---------------------------------------------

CREATE OR REPLACE FUNCTION CK_SALE_SF(
    p_date   IN  date ,
    p_product_id   IN   BB_PRODUCT.IDPRODUCT%TYPE)
    RETURN STRING     
    IS 
    v_row   BB_PRODUCT%ROWTYPE;
BEGIN
   SELECT * INTO v_row
   FROM  BB_PRODUCT
   WHERE idproduct = p_product_id; 
   IF p_date between v_row.salestart and v_row.saleend then 
       return   'ON SALE!';
   ELSE      
       return    'Great Deal';
   END IF;     
END;
/

----executing task 6 Function -----
DECLARE
  v_msg  VARCHAR2(20 BYTE)  ;
BEGIN
  v_msg := CK_SALE_SF( '17-JUN-12',25 );
  DBMS_OUTPUT.PUT_LINE(v_msg);
END;
/


--------------------------------------------
----- Report 1 -----------------
------------------------------------------
CREATE OR REPLACE PROCEDURE STOCK_CHECK( 
    p_basket_id  IN  number)
IS    
   CURSOR cur_basket IS
    SELECT bi.idbasket,bi.quantity,p.stock
    FROM   bb_basketitem bi INNER JOIN bb_product p
    USING  (idproduct)
    WHERE  bi.idbasket = 6;
  TYPE   type_basket IS RECORD (
  basket bb_basketitem.idbasket%TYPE,
  qty    bb_basketitem.quantity%TYPE,
  stock    bb_product.stock%TYPE);
  rec_basket  type_basket;
  lv_flag_txt  char(1) :='Y';
BEGIN 
    FOR frec_basket IN cur_basket 
    LOOP 
        IF rec_basket.stock < rec_basket.qty THEN lv_flag_txt:='N';END IF;
    END LOOP;
    
    IF lv_flag_txt = 'Y' THEN DBMS_OUTPUT.PUT_LINE('All items in stock!'); END IF;
    IF lv_flag_txt = 'N' THEN DBMS_OUTPUT.PUT_LINE('All items NOT in stock!'); END IF;

END;
/
--------------------------------------------
----------Report 2 Procedure---------------
---------------------------------------------
CREATE OR REPLACE FUNCTION TOT_PURCH_SF( 
    p_shopper_id  IN  number)
    RETURN NUMBER
  IS 
  v_total   NUMBER;
BEGIN 
    SELECT SUM(TOTAL) INTO v_total 
    FROM  BB_BASKET
    WHERE IDSHOPPER = p_shopper_id;
    RETURN  v_total;
END;
/

-----------EXECUTE REPORT 2  FUNCTION -----------
SELECT IDSHOPPER, TOT_PURCH_SF(IDSHOPPER)
FROM BB_SHOPPER