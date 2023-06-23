drop trigger increase_numofprod;
drop trigger updateCustWallet;
drop trigger updateStock; 

#Trigger 1
CREATE TRIGGER increase_numofprod 
AFTER INSERT 
ON contains FOR EACH ROW 
UPDATE cart SET NO_OF_PRODUCT =  NO_OF_PRODUCT + 1 where cart.Cart_Id = NEW.Cart_Id;

#Test Trigger 1
select * from cart where cart_id=37;
insert into contains values(12, 37, 25);
select * from cart where cart_id=37;

#Trigger 2
delimiter //
CREATE  TRIGGER updateCustWallet
            AFTER UPDATE
            ON `return` FOR EACH ROW
            BEGIN 
              IF (NEW.status = 'done')
              THEN
UPDATE customer set customer.wallet=customer.wallet+new.refund_amount where customer.customer_id=new.customer_id;
     END IF;
 END; //
 
 #Test Trigger 2
select * from `return`;
select * from customer where customer_id=36;
update `return` set status='done' where order_id=18;
select * from customer where customer_id=36;
 
 #Trigger 3
 delimiter //
CREATE  TRIGGER updateStock
            AFTER INSERT
            ON `order` FOR EACH ROW
            BEGIN
            IF(new.cart_id is not null)
            THEN
update product set stock=stock-1 where product_id in (select Product_Id from contains where cart_id = new.cart_id) and stock>0;
			END IF;
 END; //
 
#Test Trigger 3
select * from contains where cart_id=45;
select * from product where product_id=3;
select * from product where product_id=65;
insert into `order` values(140, 45, 40, 32, "2022-11-15 19:59:08", 678, 21, "Delhi");
select * from product where product_id=3;
select * from product where product_id=65;

