import random

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
    3->Delete category
    4->Delete product
    5->Assign delivery agent to an order
    6->View all customer queries
    7->Resolve queries
    8->Track Order
    9->Analysis of the Application 
    10->See the Working of the Triggers
    11->Complete Return
    12->Set Price of a Product
    13->Update Stock
    14->Update Contact Details
    15->Set discount on a product
    16->Back
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
    elif(n==2):
        prodName=input("Please enter the product name: ")
        mycursor.execute("select max(product_Id) from product")
        result=mycursor.fetchall()
        prodId=result[0][0]
        prodId+=1
        categName=input("Please enter category name: ")
        mycursor.execute("select category_Id from category where Name=(%s)", (categName, ))
        result=mycursor.fetchall()
        categId=result[0][0]
        price=int(input("Please enter the price of the product: "))
        disc=int(input("Please enter the discount on the product"))
        stock=int(input("Please enter the stock of the product: "))
        about=categName
        mycursor.execute("insert into product values((%s), (%s), (%s), (%s), (%s), (%s), (%s))", (prodId, prodName, disc, price, stock, about, categId))
        print("The Product has been successfully addes to the database under the category", categName)
        print("Product ID: ", prodId)
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==3):
        categId=int(input("Please enter the category ID of the category to be deleted: "))
        mycursor.execute("select * from category where category_Id=(%s)", (categId, ))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("Invalid category ID, please try again")
        else:
            mycursor.execute("delete from category where category_Id=(%s)", (categId, ))
            print("The category alongwith all the products in that category have been deleted")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==4):
        prodId=int(input("Please enter the product ID of the product to be deleted: "))
        mycursor.execute("select * from product where product_Id=(%s)", (prodId, ))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("Invalid product ID, please try again")
        else:
            mycursor.execute("delete from product where product_Id=(%s)", (prodId, ))
            print("The product has been deleted")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==5):
        orderId=int(input("Please enter the order_Id to be assigned: "))
        mycursor.execute("select agent_Id from delivery_agent where status='available'")
        result=mycursor.fetchall()
        agentId=int(result[0][0])
        status="occupied"
        mycursor.execute("update delivery_agent set status=(%s) where agent_Id=(%s)", (status, agentId))
        print("The order has been assigned to agent having agent_Id", agentId)
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==6):
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
        mycursor.execute("update customer_query set status='resolved' where admin_Id=(%s)", (adminId, ))
        print("All unresolved queries have been resolved")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==8):
        mycursor.execute("select order_id, customer_id, admin_Id, order_date, location from `order` where admin_Id=(%s)", (adminId, ))
        result=mycursor.fetchall()
        for row in result:
            print("Order_Id:", row[0])
            print("Customer_Id:", row[1])
            print("Admin_Id: ", row[2])
            print("Order_Date:", row[3])
            print("Location: ", row[4])
            print()
        adminMenu(adminId, username)
    elif(n==9):
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
    elif(n==10):
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
    elif(n==11):
        mycursor.execute("update `return` set status='done' where order_Id in (select order_id from `order` where admin_Id=(%s))", (adminId, ))
        print("All the returns have been completed!")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==12):
        prodId=int(input("Please enter product_Id: "))
        price=int(input("Please enter the new price for this product: "))
        mycursor.execute("update product set price=(%s) where product_Id=(%s)", (price, prodId))
        mydb.commit()
        print("The price of the product with product_Id", prodId, "has been updated to", price)
        adminMenu(adminId, username)
    elif(n==13):
        prodId=int(input("Please enter product_Id: "))
        stock=int(input("Please enter the new stock for this product: "))
        mycursor.execute("update product set stock=(%s) where product_Id=(%s)", (stock, prodId))
        mydb.commit()
        print("The stock of the product with product_Id", prodId, "has been updated to", stock)
        adminMenu(adminId, username)
    elif(n==14):
        mycursor.execute("select contact from admin_contact where admin_Id=(%s)", (adminId, ))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("Currently no contact number added")
        else:
            i=0
            for row in result:
                i+=1
                print("Contact", i, ":", row[0])
            print()
        q=input("Do you want to add a new contact(Y/N)?: ")
        if(q=="Y"):
            cont=input("Please enter your contact number to be added: ")
            mycursor.execute("insert into admin_contact values((%s), (%s))", (adminId, cont))
            print("Your contact number has been successfully added")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==15):
        prodId=int(input("Please enter the product ID:"))
        disc=int(input("Please enter the discount value to be set: "))
        if(disc<0 or disc>100):
            print("Invalid discount, please try again")
        else:
            mycursor.execute("update product set discount=(%s) where product_Id=(%s)", (disc, prodId))
            print("The discount on the product has been successfully updated")
        mydb.commit()
        adminMenu(adminId, username)
    elif(n==16):
        homeScreen()

def agentMenu(agentId, username):
    print("Hi,", username, "!")
    print('''Please enter:
    1->View assigned orders/returns
    2->View your ratings
    3->Update Contact Details
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
    elif(n==2):
        mycursor.execute("select rating from delivery_agent where agent_Id=(%s)", (agentId, ))
        result=mycursor.fetchall()
        rating=result[0][0]
        print("Your average rating is:", rating, "/ 5 stars ")
        agentMenu(agentId, username)
    elif(n==3):
        mycursor.execute("select contact from agent_contact where agent_Id=(%s)", (agentId, ))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("Currently no contact number added")
        else:
            i=0
            for row in result:
                i+=1
                print("Contact", i, ":", row[0])
            print()
        q=input("Do you want to add a new contact(Y/N)?: ")
        if(q=="Y"):
            cont=input("Please enter your contact number to be added: ")
            mycursor.execute("insert into agent_contact values((%s), (%s))", (agentId, cont))
            print("Your contact number has been successfully added")
        mydb.commit()
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
    5->Delete from Cart
    6->Add to Wallet
    7->Upgrade Membership
    8->Change Address
    9->Change Account Password
    10->Track Order
    11->Raise Query
    12->Place order
    13->Update Contact Details
    14->Back
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
        x=input("Do you want to apply any filters(Y/N): ")
        if(x=="Y"):
            catId=int(input("Please enter the category ID: "))
            mycursor.execute("select category_Id from category where category_Id=(%s)", (catId, ))
            result=mycursor.fetchall()
            if(len(result)==0):
                print("Incorrect Category ID, please try again")
            else:
                mycursor.execute("select product_id, name, price, discount from product where category_Id=(%s)", (catId, ))
                result2=mycursor.fetchall()
                count=0
                for row in result2:
                    print("Product Id:", row[0])
                    print("Product Name:", row[1])
                    print("Price: ", row[2],"$")
                    print("Discount:", row[3],"%")
                    print()
                    count+=1
                print("No of products:", count)
        else:
            mycursor.execute("select product_id, name, price, discount from product")
            result2=mycursor.fetchall()
            count=0
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
        mycursor.execute("select cart_Id from cart where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        cartId=int(result[0][0])
        mycursor.execute("drop view orderContains")
        mycursor.execute("create view orderContains as select product_id from contains where customer_id=(%s) and cart_Id=(%s)", (custId, cartId))
        mycursor.execute("select product.product_id, product.name, product.price, product.about from orderContains inner join product on product.product_id=orderContains.product_id")
        result3=mycursor.fetchall()
        price=0
        for row in result3:
            print("Product Id:", row[0])
            print("Product Name:", row[1])
            print("Price: ", row[2],"$")
            print("About:", row[3])
            print()
            price+=int(row[2])
        mycursor.execute("select sum(price) from orderContains inner join product on product.product_id=orderContains.product_id")
        result3=result3=mycursor.fetchall()
        print("Cart Total Price:", price,"$")
        customerMenu(custId, username)
    elif(n==4):
        mycursor.execute("select cart_Id from cart where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        cartId=int(result[0][0])
        prodId=int(input("Please enter product Id: "))
        mycursor.execute("select stock from product where product_Id=(%s)", (prodId, ))
        result=mycursor.fetchall()
        stock=result[0][0]
        adminId=random.randint(1, 100)
        if(stock>0):
            mycursor.execute("insert into contains values((%s), (%s), (%s));", (custId, cartId, prodId))
            print("Product has been successfully added to cart")
            mydb.commit()
        else:
            print("Sorry, The product you selected is out of stock!")
        customerMenu(custId, username)
    elif(n==5):
        mycursor.execute("select cart_Id from cart where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        cartId=int(result[0][0])
        prodId=int(input("Please enter product Id of the product to be deleted: "))
        mycursor.execute("select * from contains where customer_Id=(%s) and cart_Id=(%s) and product_Id=(%s)", (custId, cartId, prodId))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("There is no such product in your cart, please try again")
        else:
            mycursor.execute("delete from contains where customer_Id=(%s) and cart_Id=(%s) and product_Id=(%s)", (custId, cartId, prodId))
        mydb.commit()
        customerMenu(custId, username)
    elif(n==6):
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
    elif(n==7):
        mycursor.execute("select membership from customer where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        print("Your current membership:", result[0][0])
        q=input("Would you like to upgrade your membership(Y/N)?: ")
        mycursor.execute("select wallet from customer where customer_Id=(%s)", (custId, ))
        wallet=mycursor.fetchall()[0][0]
        if(q=="Y"):
            print("Here are the available membership options: ")
            print("Normal - Default")
            print("Prime - 50$")
            print("Elite - 100$")
            memb=input("Which membership would you like to have?: ")
            if(memb=="Normal"):
                cost=0
            elif(memb=="Prime"):
                cost=50
            elif(memb=="Elite"):
                cost=100
            if(wallet<cost):
                print("You don't have sufficient funds!")
            else:
                mycursor.execute("update customer set membership=(%s) where customer_Id=(%s)", (memb, custId))
                mycursor.execute("update customer set wallet=wallet-(%s) where customer_Id=(%s)", (cost, custId))
                print("Your Membership has been upgraded to", memb)
        mydb.commit()
        customerMenu(custId, username)
    elif(n==8):
        mycursor.execute("select address from customer where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        print("Your current address:", result[0][0])
        addr=input("Enter your new address: ")
        mycursor.execute("update customer set address=(%s) where customer_Id=(%s)", (addr, custId))
        print("Your address has been updated")
        mydb.commit()
        customerMenu(custId, username)
    elif(n==9):
        mycursor.execute("select password from customer where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        oldpass=input("Please enter your old password: ")
        if(oldpass==result[0][0]):
            newpass=input("Please enter your new password: ")
            mycursor.execute("update customer set password=(%s) where customer_Id=(%s)", (newpass, custId))
            mydb.commit()
            print("Your password has succesfully changed")
        else:
            print("Incorrect password, please retry")
        customerMenu(custId, username)
    elif(n==10):
        mycursor.execute("select order_id, customer_id, admin_Id, order_date, location from `order` where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        for row in result:
            print("Order_Id:", row[0])
            print("Customer_Id:", row[1])
            print("Admin_Id: ", row[2])
            print("Order_Date:", row[3])
            print("Location: ", row[4])
            print()
        customerMenu(custId, username)
    elif(n==11):
        mycursor.execute("select max(query_Id) from customer_query")
        result=mycursor.fetchall()
        id=int(result[0][0])
        id+=1
        adminId=random.randint(1, 100)
        desc=input("Please write the description of your query: ")
        status="raised"
        mycursor.execute("insert into CUSTOMER_QUERY (Query_Id, Description, Status, Customer_Id, Admin_Id) values (%s, %s, %s, %s, %s);", (id, desc, status, custId, adminId))
        print("Your query has been raised successfully")
        print("The admin assigned to your query has ID: ", adminId)
        mydb.commit()
        customerMenu(custId, username)
    elif(n==12):
        mycursor.execute("select max(order_Id) from `order`")
        result=mycursor.fetchall()
        od=result[0][0]
        od+=1
        mycursor.execute("select max(payment_Id) from payment")
        result=mycursor.fetchall()
        payId=result[0][0]
        payId+=1
        mycursor.execute("select cart_Id from cart where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        cartId=int(result[0][0])
        adminId=random.randint(1, 100)
        mycursor.execute("drop view v")
        mycursor.execute("create view v as select product_id from contains where customer_id=(%s) and cart_Id=(%s)", (custId, cartId))
        mycursor.execute("select product.price from v inner join product on product.product_id=v.product_id")
        price=0
        result=mycursor.fetchall()
        for row in result:
            price+=int(row[0])
        print("Your Order total is:", price)
        print("Please choose method of payment: ")
        print("1) Debit Card")
        print("2) Credit Card")
        print("3) UPI")
        print("4) Netbanking")
        print("5) COD")
        q=int(input())
        if(q==1):
            method="Debit Card"
        elif(q==2):
            method="Credit Card"
        elif(q==3):
            method="UPI"
        elif(q==4):
            method="Netbanking"
        elif(q==5):
            method="COD"
        result3=mycursor.fetchall()
        disc=random.randint(1, 99)
        mycursor.execute("Select wallet from customer where customer_Id=(%s)", (custId, ))
        result=mycursor.fetchall()
        wallet=result[0][0]
        flag=False
        if(wallet>=price):
            flag=True
            status="successful"
            mycursor.execute("update customer set wallet=wallet-(%s) where customer_Id=(%s)", (price, custId))
        else:
            print("Not sufficient funds")
            status="unsuccessful"
        date="2023-04-20 19:59:08"
        mycursor.execute("insert into `order` values((%s), (%s), (%s), (%s), ('2023-04-20 19:59:08'), (%s), (%s), ('Delhi'));", (od, cartId, custId, adminId, price, disc))
        mycursor.execute("insert into payment values((%s), (%s), (%s), (%s), (%s), (%s), (%s));", (payId, od, price, status, method, date, custId))
        if(flag):
            print("Congratulations, your order has been successfully placed!")
        mydb.commit()
        customerMenu(custId, username)
    elif(n==13):
        mycursor.execute("select contact from customer_contact where customer_Id=(%s);", (custId, ))
        result=mycursor.fetchall()
        if(len(result)==0):
            print("Currently no contact number added")
        else:
            i=0
            for row in result:
                i+=1
                print("Contact", i, ":", row[0])
            print()
        q=input("Do you want to add a new contact(Y/N)?: ")
        if(q=="Y"):
            cont=input("Please enter your contact number to be added: ")
            mycursor.execute("insert into customer_contact values((%s), (%s));", (custId, cont))
            print("Your contact number has been successfully added")
        mydb.commit()
        customerMenu(custId, username)
    # elif(n==14):
    #     prodId=int(input("Please enter the product ID of the product you want to rate: "))
    #     stars=float(input("Please rate the product in stars out of 5: "))
    #     mycursor.execute("select * from product where product_Id=(%s)", (prodId, ))
    #     result=mycursor.fetchall()
    #     if(len(result)!=0):
    #         if(stars<2.5):
    #             desc="negative review"
    #         else:
    #             desc="positive review"
    #         mycursor.execute("insert into review values((%s), (%s), (%s), (%s))", (prodId, custId, stars, desc))
    #         print("You have successfully rated the product")
    #     mydb.commit()
    #     customerMenu(custId, username)
    elif(n==14):
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
                # print("Wrong username or password, Please retry!")
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
                # print("Wrong username or password, Please retry!")
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

# customerMenu(59, "pompom") tvkuu9GZnN
# adminMenu(1, "pompom")  0o8zeXPH
# agentMenu(Dennis Dodds, "pompom")
homeScreen()
    


