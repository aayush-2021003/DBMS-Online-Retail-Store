# DBMS-Online-Retail-Store
Using Python language and MYSQL, created an online retail store implementing the database concepts ensuring atomicity, consistency, isolation and durability.

### Scope:
<img width="126" alt="2023-07-11 (2)" src="https://github.com/aayush-2021003/DBMS-Online-Retail-Store/assets/108550892/d40865af-12bd-413f-a2b3-6107a755f193">

Today, due to the extremely fast-paced lives of people, it can be exhausting and time-consuming
to visit different stores at different locations. Visiting a market and choosing the right product is
cumbersome and may take several hours. Also, due to the recent COVID-19 pandemic, people
prefer to get products delivered to their doorstep as quickly as possible.
Therefore, to cater to the needs of the public, we provide complete management solutions to
manage information on customers, sellers, delivery agents and products efficiently.
A2Z gives the admins a forum to showcase their products of various categories to customers in
a hassle-free and systematic way. Customers can conveniently browse products, manage items
in the cart and buy as per their preferred payment method. Delivery agents are assigned orders
by the admin, which are supposed to be delivered within the stipulated time to provide an
excellent experience to customers. Each of the objects is identified by a unique attribute, i.e.,
their primary key - Customer_ID, Admin_ID, Delivery_Agent_ID, Order_ID, Product_ID and so
on.
This application will enable the admin, delivery agent and customer to interact and coordinate
efficiently with each other, resulting in a pleasant experience for all.


### USER GUIDE:

### Functionalities:

### Customers can do the following:
- Sign Up/Login: The customer can either create a new account or login with their
unique credentials.
- Show all Categories: The customer can see all the available categories on the
application
- Browse products: The customer can browse for the products they want.
- Add filters: They can also add filters while searching to get their desired
products quicker.
- View items of Cart: The customer can view all the items added to the cart by the
customer.
- Add/Delete product in the cart: The customer can add/delete products to/from
their cart.
- Buy products: The customers can buy the products in their cart by clicking on
the “Place Order” button.
- View/Update Account Balance: Customers can view their account balance and
also add money to their account if needed.
- Make payments: Customers can make the payment after clicking on the “Place
Order” button and then choosing their desired payment option.
- Return Product: Customers can choose to return any product if they want.
There is a no questions asked return and refund policy.
- Track Order: Customers can choose to track their order(Number of days for
delivery, Location of the order, etc.).
- Raise query: Customers can also raise queries/concerns regarding anything on
the app which are answered by admins.
- Upgrade membership : The membership of the customer can be changed
- Change Address : The address of the customer initially entered can be
updated.
- Change account Password : The password of the customer initially entered can
be changed.
- Update Contact Details: The Customer can add their contact details on the
system and also check their existing contact details on the system.

### Admin can do the following:
- Login: The admin will have to enter their unique credentials to access the Admin
mode
- Add/Delete Category: Any category can be added or deleted by the admin once
the admin mode is activated.
- Add/Delete Product: Any product can be added or deleted by the admin in the
suitable category.
- Set Price: The price of the products can be edited by the admin.
- Set Discount: Different products can have various discounts as per the admin’s
choice.
- Update Stock: This enables them to update the logistics and maintain the
correct record of their inventory. Eg, the number of items available, the number of
pending orders and so on.
- Assign Delivery Agent to an order/return: The admin can assign the pending
deliveries to any of the available delivery agents, be it an order or a return
request.
- Track Orders: The delivery agent can be tracked, and the location of the order
can be located in real-time by the admin.
- Reply to Customer Queries: They’ll be able to view all the queries raised by the
customers so that they can reply to them accordingly.
- Resolve Queries: Mark the status of of the queries as “resolved” belonging to a
particular admin_id
- Analysis of the application : This provides various forms of analysis of the
logistics of the database and can help in their study and a better understanding.
- Working of Triggers : To show working of the triggers for the deadline 5
- Complete Return : Mark the returns as “done” for a specific admin id
- Update Contact Details : This allows them to regularly change and maintain the
correct contact details for the user.

### Delivery Agent:
- Login: The delivery agent can log in with their unique credentials.
- View the assigned order/return: They can view the order/ return assigned to
them by the admin.
- View their rating: They can view the rating given to them by the customers.
- Update contact details: This allows them to regularly change and maintain the
correct contact details for the user.

### Schema
### CUSTOMER
- Customer_Id: Integer NOT NULL UNIQUE
- Name: VARCHAR(50) NOT NULL
- Username: VARCHAR(50) NOT NULL UNIQUE
- Password: VARCHAR(50) NOT NULL
- Address: VARCHAR(50) NOT NULL
- Membership: VARCHAR(6)
- Wallet: Integer NOT NULL
- primary key: Customer_Id
- constraint: cust_wallet check(Wallet>=0)

### ADMIN
- Admin_Id: Integer NOT NULL UNIQUE
- Name: VARCHAR(50) NOT NULL
- Company_Name: VARCHAR(50) NOT NULL
- Username: VARCHAR(50) NOT NULL UNIQUE
- Password: VARCHAR(100) NOT NULL
- Contact: VARCHAR(50) NOT NULL UNIQUE
- primary key: Admin_Id

### CATEGORY
- Category_Id: Integer NOT NULL UNIQUE
- Name: VARCHAR(50) NOT NULL UNIQUE
- No_Of_Products: Integer NOT NULL
- primary key: Category_Id
- constraint: categ_num check(No_Of_Products>=0)

### PRODUCT
- Product_Id: Integer NOT NULL UNIQUE
- Name: VARCHAR(50) NOT NULL
- Discount: Integer
- Price: Integer NOT NULL
- Stock: Integer NOT NULL
- About: VARCHAR(100)
- Category_Id: Integer NOT NULL
- primary key: Product_Id
- foreign key: Category_Id references CATEGORY(Category_Id) on delete cascade
- constraint: prod_stock check(Stock>=0)
- constraint: prod_price check(Price>0)
- constraint: prod_disc check(Discount>=0)

### CUSTOMER_QUERY
- Query_Id: Integer NOT NULL UNIQUE
- Description: VARCHAR(26) NOT NULL
- Status: VARCHAR(8) NOT NULL
- Customer_Id: Integer NOT NULL
- Admin_Id: Integer NOT NULL
- primary key: Query_Id
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- foreign key: Admin_Id references ADMIN(Admin_Id) on delete cascade

  ### CART
- Cart_Id: Integer NOT NULL UNIQUE
- No_Of_Product: Integer NOT NULL
- Customer_Id: Integer NOT NULL
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- constraint: cart_qty check(No_Of_Product>=0)

- ### 'ORDER'
- Order_Id: Integer NOT NULL UNIQUE
- Cart_Id: Integer NOT NULL
- Customer_Id: Integer NOT NULL
- Admin_Id: Integer NOT NULL
- Order_Date: DATETIME NOT NULL
- Total_Price: Integer NOT NULL
- Total_Discount: Integer
- Location: VARCHAR(50) NOT NULL
- primary key: Order_Id
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- foreign key: Admin_Id references ADMIN(Admin_Id) on delete cascade
- constraint: order_price check(Total_Price>=0)
- constraint: order_disc check(Total_Discount>=0)

### DELIVERY_AGENT
- Agent_Id: Integer NOT NULL UNIQUE
- Order_Id: Integer NOT NULL
- Admin_Id: Integer NOT NULL
- Name: VARCHAR(50) NOT NULL
- Status: VARCHAR(9) NOT NULL
- Rating: DECIMAL(2,1) NOT NULL
- primary key: Agent_Id
- foreign key: Order_Id references `ORDER`(Order_Id) on delete cascade
- foreign key: Admin_Id references Admin(Admin_Id) on delete cascade
- constraint: agent_rate check(Rating>=1 and Rating<=5)

### 'RETURN'
- Order_Id: Integer NOT NULL UNIQUE
- Status: VARCHAR(9) NOT NULL
- Refund_Amount: Integer NOT NULL
- Customer_Id: Integer NOT NULL
- Agent_Id: Integer NOT NULL
- Contact: VARCHAR(50) NOT NULL
- foreign key: Order_Id references `ORDER`(Order_Id)
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- foreign key: Agent_Id references DELIVERY_AGENT(Agent_Id) on delete cascade
- constraint: return_refund check(Refund_Amount>=0)

### PAYMENT
- Payment_Id: Integer NOT NULL UNIQUE
- Order_Id: Integer NOT NULL
- Price: Integer NOT NULL
- Status: VARCHAR(10) NOT NULL
- Payment_Method: VARCHAR(11) NOT NULL
- Payment_Date: DATETIME NOT NULL
- Customer_Id: Integer NOT NULL
- primary key: Payment_Id
- foreign key: Order_Id references `ORDER`(Order_Id) on delete cascade
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- constraint: payment_price check(Price>=0)

### REVIEW
- Product_Id: Integer NOT NULL
- Customer_Id: Integer NOT NULL
- Stars: DECIMAL(2,1) NOT NULL
- Description: VARCHAR(15)
- foreign key: Product_Id references PRODUCT(Product_Id) on delete cascade
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- constraint: review_stars check(Stars>=1 and Stars<=5)

### SUPPLIES
- Admin_Id: Integer NOT NULL
- Product_Id: Integer NOT NULL
- foreign key: Admin_Id references ADMIN(Admin_Id) on delete cascade
- foreign key: Product_Id references PRODUCT(Product_Id) on delete cascade

### RATES
- Customer_Id: Integer NOT NULL
- Agent_Id: Integer NOT NULL
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- foreign key: Agent_Id references DELIVERY_AGENT(Agent_Id) on delete cascade
    
### CONTAINS
- Customer_Id: Integer NOT NULL
- Cart_Id: Integer NOT NULL
- Product_Id: Integer NOT NULL
- foreign key: Customer_Id references CUSTOMER(Customer_Id) on delete cascade
- foreign key:  Product_Id references PRODUCT(Product_Id) on delete cascade

### ADMIN_CONTACT
- Admin_Id: Integer NOT NULL
- Contact: VARCHAR(50) NOT NULL
- foreign key: Admin_Id references ADMIN(Admin_Id)

### CUSTOMER_CONTACT
- Customer_Id: Integer NOT NULL
- Contact: VARCHAR(50) NOT NULL
- foreign key: Customer_Id references CUSTOMER(Customer_Id)

### AGENT_CONTACT
- Agent_Id: Integer NOT NULL
- Contact: VARCHAR(50) NOT NULL
- foreign key: Agent_Id references DELILVERY_AGENT(Agent_Id)

### CART_PRODUCT
- Cart_Id: Integer NOT NULL
- Customer_Id: Integer NOT NULL
- Product_Id: Integer NOT NULL
- foreign key: Customer_Id references CUSTOMER(Customer_Id)
- foreign key: Product_Id references PRODUCT(Product_Id)
