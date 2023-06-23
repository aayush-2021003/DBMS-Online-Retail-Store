def addCust(name, user, passwd, address, membership, wallet):
    mycursor.execute("select max(customer_id) from customer")
    result=mycursor.fetchall()
    id=int(result[0][0])
    id+=1
    mycursor.execute("insert into customer values(%s, %s, %s, %s, %s, %s, %s)", (id, name, user, passwd, address, membership, wallet))
    mydb.commit()
    return id

def addAdmin(name, compName, user, passwd, contact):
    mycursor.execute("select max(admin_Id) from admin")
    result=mycursor.fetchall()
    id=int(result[0][0])
    id+=1
    mycursor.execute("insert into admin values(%s, %s, %s, %s, %s, %s)", (id, name, compName, user, passwd, contact))
    mydb.commit()
    return id
def authenticate(user, passwd, type):
    if(type=="customer"):
        mycursor.execute("select customer_id from customer where username=(%s) and password=(%s)", (user, passwd))
    elif(type=="admin"):
        mycursor.execute("select admin_Id from admin where username=(%s) and password=(%s)", (user, passwd))
    elif(type=="agent"):
        mycursor.execute("select agent_id from delivery_agent where name=(%s)", (user, ))
    result=mycursor.fetchall()
    if(len(result)==0):
        print("Wrong username or password, Please retry")
    else:
        id=int(result[0][0])
        return id

def adminMenu(adminId, username):
    print("Hi,", username, "!")
    print('''Please enter:
    1->Add category
    2->Add product
    3->Assign delivery agent
    4->View all customer queries
    5->Resolve queries
    6->Track Order
    7->Analysis of the Application 
    8->See the Working of the Triggers
    9->Back
    ''')
    n=int(input())
    if(n==1):
        categName=input("Please enter category name: ")
        mycursor.execute("select max(category_Id) from category")
        result5=mycursor.fetchall()
        categId=int(result5[0][0])
        categId+=1
        mycursor.execute("insert into category values(%s, %s, %s)", (categId, categName, 1))
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==4):
        mycursor.execute("select * from customer_query where admin_id=(%s)", (adminId, ))
        result6=mycursor.fetchall()
        count=0
        for row in result6:
            print("Query_Id:", row[0])
            print("Description:", row[1])
            print("Status: ", row[2])
            if(row[2]!="resolved"):
                count+=1
            print("Customer_Id:", row[3])
            print("Admin:", row[3])
            print()
        print(count,"/",len(result6),"queries unresolved")
        adminMenu(adminId, username)
    elif(n==7):
        print('''Please enter:
        1->Display the average rating using Grouping Sets
        2->Display the average rating using Cube
        3->Display no of orders placed grouped by year and month
        4->Display the revenue made by the application grouped by year, month and method of payment
        5->Display the number of returns grouped by customer_id and status of the return
        ''')
        option=int(input())
        if(option==1):
            mycursor.execute("drop view v1;")
            mycursor.execute("drop view v2;")
            mycursor.execute("create view v1 as select customer_id, product_id, avg(stars) as av from review group by customer_id, product_id with ROLLUP;")
            mycursor.execute("create view v2 as select customer_id, product_id, avg(stars) as av from review group by product_id, customer_id with ROLLUP;")
            mycursor.execute("drop view unio;")
            mycursor.execute("create view unio as select customer_id, product_id, avg(stars) as av from review group by customer_id, product_id with ROLLUP UNION select customer_id, product_id, avg(stars) as av from review group by product_id, customer_id with ROLLUP;")
            mycursor.execute("drop view inter;")
            mycursor.execute("create view inter as SELECT DISTINCT customer_id, product_id, av FROM v1  INNER JOIN v2 USING(customer_id, product_id, av);")
            mycursor.execute("select DISTINCT unio.customer_id, unio.product_id, unio.av from unio inner join inter where unio.customer_id is NULL and inter.customer_id is not NULL or unio.product_id is null and inter.product_id is not null;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            adminMenu(adminId, username)
        elif(option==2):
            mycursor.execute("select customer_id, product_id, avg(stars) from review group by customer_id, product_id with ROLLUP UNION select customer_id, product_id, avg(stars) from review group by product_id, customer_id with ROLLUP;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            adminMenu(adminId, username)
        elif(option==3):
            mycursor.execute("select EXTRACT(YEAR FROM order_date) as year, EXTRACT(MONTH FROM order_date) as month, count(order_id) from `order` group by  EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date) with ROLLUP;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            adminMenu(adminId, username)
        elif(option==4):
            mycursor.execute("select payment_method, EXTRACT(YEAR FROM payment_date) as year, EXTRACT(MONTH FROM payment_date) as month, sum(price) from payment group by  payment_method, EXTRACT(YEAR FROM payment_date), EXTRACT(MONTH FROM payment_date) with ROLLUP;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            adminMenu(adminId, username)
        elif(option==5):
            mycursor.execute("select customer_id, status, count(order_id) from `return` group by customer_id, status with ROLLUP;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            adminMenu(adminId, username)
    elif(n==8):
        print('''Please enter:
        1->Add to Cart Trigger
        2->Update customer wallet after refund
        3->Place an Order Trigger''')
        option=int(input())
        if(option==1):
            mycursor.execute("select * from contains where cart_id=45;")
            result=mycursor.fetchall()
            for row in result:
                print(row)
            mycursor.execute("select stock from product where product_id=3;")
            result=mycursor.fetchall()
            print("Initial Stock:", result[0][0])
            mycursor.execute("select stock from product where product_id=65;")
            result=mycursor.fetchall()
            print("Initial Stock:", result[0][0])
            mycursor.execute("insert into `order` values(150, 45, 40, 32, '2022-11-15 19:59:08', 678, 21, 'Delhi');")
            mycursor.execute("select stock from product where product_id=3;")
            result=mycursor.fetchall()
            print("Final Stock:", result[0][0])
            mycursor.execute("select stock from product where product_id=65;")
            result=mycursor.fetchall()
            print("Final Stock:", result[0][0])
            adminMenu(adminId, username)
        elif(option==2):
            # mycursor.execute("select * from `return`;")
            mycursor.execute("select wallet from customer where customer_id=36;")
            result=mycursor.fetchall()
            print("Initial Amount in the wallet:", result[0][0])
            mycursor.execute("update `return` set status='done' where order_id=18;")
            mycursor.execute("select refund_amount from `return` where order_id=18;")
            result=mycursor.fetchall()
            print("Refund amount:", result[0][0])
            mycursor.execute("select wallet from customer where customer_id=36;")
            result=mycursor.fetchall()
            print("Final Amount in the wallet:", result[0][0])
            adminMenu(adminId, username)
        elif(option==3):
            mycursor.execute("select no_of_product from cart where cart_id=37;")
            result=mycursor.fetchall()
            print("Initial Cart size:", result[0][0])
            mycursor.execute("insert into contains values(12, 37, 25);")
            mycursor.execute("select no_of_product from cart where cart_id=37;")
            result=mycursor.fetchall()
            print("Final Cart size:", result[0][0])
            adminMenu(adminId, username)
    elif(n==9):
        homeScreen()

def agentMenu(agentId, username):
    print("Hi,", username, "!")
    print('''Please enter:
    1->View assigned orders/returns
    2->View your ratings
    3->View completed deliveries
    4->Back
    ''')
    n=int(input())
    if(n==1):
        print("Orders: ")
        mycursor.execute("select count(order_id) from delivery_agent where agent_id=(%s)", (agentId, ))
        result7=mycursor.fetchall()
        print(result7[0][0])
        mycursor.execute("select order_id from delivery_agent where agent_id=(%s)", (agentId, ))
        result=mycursor.fetchall()
        for row in result:
            print("Order Id:", row[0])
        print()
        print("Returns: ")
        mycursor.execute("select count(order_id) from `return` where agent_id=(%s)", (agentId, ))
        result8=mycursor.fetchall()
        print(result8[0][0])
        mycursor.execute("select order_id from `return` where agent_id=(%s)", (agentId, ))
        result=mycursor.fetchall()
        for row in result:
            print("Order Id:", row[0])
        print()
        agentMenu(agentId, username)
    elif(n==4):
        homeScreen()


def customerMenu(custId, username):
    print("Hi,", username, "!")
    print('''Please enter:
    1->Show all Categories
    2->Browse Products
    3->View Cart
    4->Add to Cart
    5->Add to Wallet
    6->Upgrade Membership
    7->Change Address
    8->Change Account Password
    9->Track Order
    10->Back
    ''')
    n=int(input())
    #Show all categs
    if(n==1):
        count=0
        mycursor.execute("select category_id, name from category")
        result1=mycursor.fetchall()
        for row in result1:
            print("Category Id:", row[0])
            print("Category Name:", row[1])
            print()
            count+=1
        print("No of categories:", count)
        customerMenu(custId, username)
    #Show all prods
    elif(n==2):
        count=0
        mycursor.execute("select product_id, name, price, discount from product")
        result2=mycursor.fetchall()
        for row in result2:
            print("Product Id:", row[0])
            print("Product Name:", row[1])
            print("Price: ", row[2],"$")
            print("Discount:", row[3],"%")
            print()
            count+=1
        print("No of products:", count)
        customerMenu(custId, username)
    elif(n==3):
        mycursor.execute("drop view orderContains")
        mycursor.execute("create view orderContains as select product_id from `order` inner join contains on `order`.cart_id=contains.cart_id  where `order`.customer_id=59")
        mycursor.execute("select product.product_id, product.name, product.price, product.about from orderContains inner join product on product.product_id=orderContains.product_id")
        result3=mycursor.fetchall()
        for row in result3:
            print("Product Id:", row[0])
            print("Product Name:", row[1])
            print("Price: ", row[2],"$")
            print("About:", row[3])
            print()
        mycursor.execute("select sum(price) from orderContains inner join product on product.product_id=orderContains.product_id")
        result3=result3=mycursor.fetchall()
        print("Cart Total Price:", result3[0][0],"$")
        customerMenu(custId, username)
    elif(n==5):
        print("Your wallet currently has: ")
        mycursor.execute("select wallet from customer where customer_id=(%s)", (custId, ))
        result4=mycursor.fetchall()
        print(result4[0][0], "$") 
        amt=int(input("Enter the amount to be added to the wallet: "))
        mycursor.execute("update customer set wallet=wallet+(%s) where customer_id=(%s)", (amt, custId))
        mydb.commit()
        mycursor.execute("select wallet from customer where customer_id=(%s)", (custId, ))
        print("Your wallet now contains: ")
        result4=mycursor.fetchall()
        print(result4[0][0], "$") 
        customerMenu(custId, username)
    elif(n==10):
            homeScreen()

def homeScreen():
    print("WELCOME TO A2Z")
    print('''Please enter:
        1->Admin
        2->Customer
        3->Delivery Agent
        4->Exit the Application''')
    option1=int(input())
    #Admin
    if(option1==1):
        print('''Please enter: 
        1->Login
        2->Signup
        3->Back''')
        n1=int(input())
        if(n1==1):
            user=input("Please enter username: ")
            passwd=input("Please enter password: ")
            ret=authenticate(user, passwd, "admin")
            if(ret!=None):
                adminMenu(ret, user)
            else:
                print("Wrong username or password, Please retry!")
                homeScreen()
        elif(n1==2):
            print("Please enter your credentials: ")
            name=input("Enter your name: ")
            compName=input("Please enter your company name: ")
            user=input("Please enter username: ")
            passwd=input("Please enter password: ")
            contact=input("Please enter your contact number")
            id=addAdmin(name, compName, user, passwd, contact)
            print("Account successfully created, Here's your admin id: ", id)
            adminMenu(id, user)
        elif(n1==3):
            homeScreen()
        #Customer
    elif(option1==2):
        print('''Please enter: 
        1->Login
        2->Signup
        3->Back''')
        n1=int(input())
        if(n1==1):
            user=input("Please enter username: ")
            passwd=input("Please enter password: ")
            ret=authenticate(user, passwd, "customer")
            if(ret!=None):
                customerMenu(ret, user)
            else:
                print("Wrong username or password, Please retry!")
                homeScreen()
        elif(n1==2):
            print("Please enter your credentials: ")
            name=input("Enter your name: ")
            user=input("Please enter username: ")
            passwd=input("Please enter password: ")
            address=input("Please enter your address: ")
            membership="NORMAL"
            wallet=0
            id=addCust(name, user, passwd, address, membership, wallet)
            print("Account successfully created, Here's your customer id: ", id)
            customerMenu(id, user)
        elif(n1==3):
            homeScreen()
        #Delivery Agent
    elif(option1==3):
        print('''Please enter: 
        1->Login
        2->Signup
        3->Back''')
        n1=int(input())
        if(n1==1):
            name=input("Please enter your Name: ")
            agentId=authenticate(name, " ", "agent")
            if(agentId!=None):
                agentMenu(agentId, name)
            else:
                homeScreen()
        #Exit
    elif(option1==4):
        print("Exiting the application")



import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="messi@181222",
  database="online_retail"
)

mycursor = mydb.cursor()

# customerMenu(59, "pompom")
# adminMenu(29, "pompom")
# agentMenu(38, "pompom")
homeScreen()
    


