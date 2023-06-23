#QUERIES:
#1
SELECT contact FROM agent_contact WHERE agent_id in (SELECT agent_id FROM delivery_agent WHERE order_id in (SELECT order_id FROM `order` WHERE customer_id=13));
#2
SELECT * FROM product ORDER BY price;
#3
Select product_id, name from product where product_id in (select product_id from contains where customer_id=76) and category_id=19;
#4
SELECT description, status FROM customer_query WHERE customer_id=76;
#5
create view customer_ord as select count(*) as orders from `order` inner join customer on `order`.customer_id=customer.customer_id where customer.customer_id=76;
create view customer_ret as select count(*) as returns from `return` inner join customer on customer.customer_id=`return`.customer_id where customer.customer_id=76;
select * from customer_ord natural join customer_ret;
#6
SELECT Stars FROM review WHERE Product_Id=75;
#7
SELECT * FROM product LEFT JOIN category USING (category_id) ORDER BY category.category_id DESC;
#8
DROP VIEW frequency;
DROP VIEW maxfrequency;
CREATE VIEW frequency AS select customer_id, COUNT(*) freq FROM payment GROUP BY customer_id;
CREATE VIEW maxfrequency AS SELECT * FROM frequency WHERE freq IN (SELECT MAX(freq) FROM frequency);
SELECT * FROM customer INNER JOIN maxfrequency ON customer.customer_id=maxfrequency.customer_id;
#9
UPDATE customer_query SET status="resolved" WHERE customer_id=30;
#10
SELECT max(price) FROM product GROUP BY category_id;
#11
SELECT product_id, name, price FROM product WHERE product_id IN (SELECT product_id FROM product WHERE Category_Id=19) ORDER BY price;
#12
SELECT COUNT(product_id) AS Num_of_products_in_each_Category FROM products GROUP BY category_id;
#13
SELECT Customer.Customer_Id, Customer.Name, Payment.Payment_Id, Payment.Price, Payment.Status FROM Payment INNER JOIN Customer ON Payment.Customer_id=Customer.Customer_id;
#14
SELECT admin_id, count(product_id) FROM supplies WHERE product_id IN (SELECT contains.product_id FROM contains INNER JOIN supplies ON supplies.product_id=contains.product_id WHERE cart_id IN (SELECT cart_id FROM `order`)) GROUP BY admin_id;
#15
select * from contains inner join product on contains.product_Id=product.product_id inner join category using (category_id) order by cart_id;