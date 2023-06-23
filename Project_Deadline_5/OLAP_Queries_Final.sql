#Grouping Sets
drop view v1;
drop view v2;
create view v1 as select customer_id, product_id, avg(stars) as av from review group by customer_id, product_id with ROLLUP;
create view v2 as select customer_id, product_id, avg(stars) as av from review group by product_id, customer_id with ROLLUP;

drop view unio;
create view unio as select customer_id, product_id, avg(stars) as av from review group by customer_id, product_id with ROLLUP
UNION
select customer_id, product_id, avg(stars) as av from review group by product_id, customer_id with ROLLUP;

drop view inter;
create view inter as SELECT DISTINCT customer_id, product_id, av FROM v1  
INNER JOIN v2 USING(customer_id, product_id, av); 

select DISTINCT unio.customer_id, unio.product_id, unio.av from unio inner join inter where unio.customer_id is NULL and inter.customer_id is not NULL or unio.product_id is null and inter.product_id is not null;


#Cube
select customer_id, product_id, avg(stars) from review group by customer_id, product_id with ROLLUP
UNION
select customer_id, product_id, avg(stars) from review group by product_id, customer_id with ROLLUP;

#ROLLUP 1
select EXTRACT(YEAR FROM order_date) as year, EXTRACT(MONTH FROM order_date) as month, count(order_id) from `order` group by  EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date) with ROLLUP;

#ROLLUP 2
select payment_method, EXTRACT(YEAR FROM payment_date) as year, EXTRACT(MONTH FROM payment_date) as month, sum(price) from payment group by  payment_method, EXTRACT(YEAR FROM payment_date), EXTRACT(MONTH FROM payment_date) with ROLLUP;

#ROLLUP 3
select customer_id, status, count(order_id) from `return` group by customer_id, status with ROLLUP;
