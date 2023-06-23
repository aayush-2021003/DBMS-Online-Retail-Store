drop table if exists PAYMENT;
drop table if exists CONTAINS;
drop table if exists SUPPLIES;
drop table if exists RATES;
drop table if exists REVIEW;
drop table if exists `RETURN`;
drop table if exists DELIVERY_AGENT;
drop table if exists `ORDER`;
drop table if exists CART;
drop table if exists CUSTOMER_QUERY;
drop table if exists CUSTOMER;
drop table if exists PRODUCT;
drop table if exists CATEGORY;
drop table if exists ADMIN;
drop table if exists AGENT_CONTACT;
drop table if exists CUSTOMER_CONTACT;
drop table if exists AGENT_CONTACT;
drop table if exists CART_PRODUCT;

create table if not exists ADMIN (
	Admin_Id Integer NOT NULL UNIQUE,
	Name VARCHAR(50) NOT NULL,
	Company_Name VARCHAR(50) NOT NULL,
	Username VARCHAR(50) NOT NULL UNIQUE,
	Password VARCHAR(100) NOT NULL,
	Contact VARCHAR(50) NOT NULL UNIQUE,
    primary key(Admin_Id)
);

create table if not exists CUSTOMER (
	Customer_Id Integer NOT NULL UNIQUE,
	Name VARCHAR(50) NOT NULL,
	Username VARCHAR(50) NOT NULL UNIQUE,
	Password VARCHAR(50) NOT NULL,
	Address VARCHAR(50) NOT NULL,
	Membership VARCHAR(6),
	Wallet Integer NOT NULL,
    primary key(Customer_Id),
    constraint cust_wallet check(Wallet>=0)
);

create table if not exists CATEGORY (
	Category_Id Integer NOT NULL UNIQUE,
	Name VARCHAR(50) NOT NULL UNIQUE,
	No_Of_Products Integer NOT NULL,
    primary key(Category_Id),
    constraint categ_num check(No_Of_Products>=0)
);

create table if not exists PRODUCT (
	Product_Id Integer NOT NULL UNIQUE,
	Name VARCHAR(50) NOT NULL,
	Discount Integer,
	Price Integer NOT NULL,
	Stock Integer NOT NULL,
	About VARCHAR(100),
	Category_Id Integer NOT NULL,
    primary key(Product_Id),
    foreign key(Category_Id) references CATEGORY(Category_Id) on delete cascade,
    constraint prod_stock check(Stock>=0),
    constraint prod_price check(Price>0),
    constraint prod_disc check(Discount>=0)
);

create table if not exists CUSTOMER_QUERY (
	Query_Id Integer NOT NULL UNIQUE,
	Description VARCHAR(26) NOT NULL,
	Status VARCHAR(8) NOT NULL,
	Customer_Id Integer NOT NULL,
	Admin_Id Integer NOT NULL,
    primary key(Query_Id),
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    foreign key(Admin_Id) references ADMIN(Admin_Id) on delete cascade
);

create table if not exists CART (
	Cart_Id Integer NOT NULL UNIQUE,
    No_Of_Product Integer NOT NULL,
    Customer_Id Integer NOT NULL,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    constraint cart_qty check(No_Of_Product>=0)
);

create table if not exists `ORDER` (
	Order_Id Integer NOT NULL UNIQUE,
	Cart_Id Integer NOT NULL,
	Customer_Id Integer NOT NULL,
	Admin_Id Integer NOT NULL,
	Order_Date DATETIME NOT NULL,
	Total_Price Integer NOT NULL,
	Total_Discount Integer,
	Location VARCHAR(50) NOT NULL,
    primary key(Order_Id),
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
	foreign key(Admin_Id) references ADMIN(Admin_Id) on delete cascade,
    constraint order_price check(Total_Price>=0),
    constraint order_disc check(Total_Discount>=0)
);

create table if not exists DELIVERY_AGENT (
	Agent_Id Integer NOT NULL UNIQUE,
	Order_Id Integer NOT NULL,
	Admin_Id Integer NOT NULL,
	Name VARCHAR(50) NOT NULL,
	Status VARCHAR(9) NOT NULL,
	Rating DECIMAL(2,1) NOT NULL,
    primary key(Agent_Id),
    foreign key(Order_Id) references `ORDER`(Order_Id) on delete cascade,
    foreign key(Admin_Id) references Admin(Admin_Id) on delete cascade,
    constraint agent_rate check(Rating>=1 and Rating<=5)
);

create table if not exists `RETURN` (
	Order_Id Integer NOT NULL UNIQUE,
	Status VARCHAR(9) NOT NULL,
	Refund_Amount Integer NOT NULL,
	Customer_Id Integer NOT NULL,
	Agent_Id Integer NOT NULL,
	Contact VARCHAR(50) NOT NULL,
    foreign key(Order_Id) references `ORDER`(Order_Id),
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    foreign key(Agent_Id) references DELIVERY_AGENT(Agent_Id) on delete cascade,
    constraint return_refund check(Refund_Amount>=0)
);

create table if not exists PAYMENT (
	Payment_Id Integer NOT NULL UNIQUE,
	Order_Id Integer NOT NULL,
	Price Integer NOT NULL,
	Status VARCHAR(10) NOT NULL,
	Payment_Method VARCHAR(11) NOT NULL,
	Payment_Date DATETIME NOT NULL,
	Customer_Id Integer NOT NULL,
    primary key(Payment_Id),
    foreign key(Order_Id) references `ORDER`(Order_Id) on delete cascade,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    constraint payment_price check(Price>=0)
);

create table if not exists REVIEW(
	Product_Id 	Integer NOT NULL,
	Customer_Id Integer NOT NULL,
	Stars DECIMAL(2,1) NOT NULL,
	Description VARCHAR(15),
    foreign key(Product_Id) references PRODUCT(Product_Id) on delete cascade,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    constraint review_stars check(Stars>=1 and Stars<=5)
);

create table SUPPLIES (
	Admin_Id Integer NOT NULL,
	Product_Id Integer NOT NULL,
    foreign key(Admin_Id) references ADMIN(Admin_Id) on delete cascade,
    foreign key(Product_Id) references PRODUCT(Product_Id) on delete cascade
);

create table if not exists RATES (
	Customer_Id Integer NOT NULL,
	Agent_Id Integer NOT NULL,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    foreign key(Agent_Id) references DELIVERY_AGENT(Agent_Id) on delete cascade
    
);

create table if not exists CONTAINS (
	Customer_Id Integer NOT NULL,
	Cart_Id Integer NOT NULL,
	Product_Id Integer NOT NULL,
	foreign key(Customer_Id) references CUSTOMER(Customer_Id) on delete cascade,
    foreign key(Product_Id) references PRODUCT(Product_Id) on delete cascade
);

create table if not exists ADMIN_CONTACT (
	Admin_Id Integer NOT NULL,
	Contact VARCHAR(50) NOT NULL,
    foreign key(Admin_Id) references ADMIN(Admin_Id)
);

create table if not exists CUSTOMER_CONTACT (
	Customer_Id Integer NOT NULL,
	Contact VARCHAR(50) NOT NULL,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id)
);

create table if not exists AGENT_CONTACT (
	Agent_Id Integer NOT NULL,
	Contact VARCHAR(50) NOT NULL,
    foreign key(Agent_Id) references DELILVERY_AGENT(Agent_Id)
);

create table if not exists CART_PRODUCT (
	Cart_Id Integer NOT NULL,
	Customer_Id Integer NOT NULL,
    Product_Id Integer NOT NULL,
    foreign key(Customer_Id) references CUSTOMER(Customer_Id),
    foreign key(Product_Id) references PRODUCT(Product_Id)
);
	