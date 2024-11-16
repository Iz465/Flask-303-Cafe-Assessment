
from operator import itemgetter
import sqlite3, sqlite_functions

class Handler():
    def __init__(self):
        self.sortingmethods = []
        self.tablevalues = []
    def sorteddata(self,data, method_sort):
        sorted_list = data
        if method_sort == self.sortingmethods[0]:
            sorted_list = sorted(data, key=itemgetter(self.tablevalues[0]))
        elif method_sort == self.sortingmethods[1]:
            sorted_list = sorted(data, key=itemgetter(self.tablevalues[1]))
        return sorted_list
    def searchdata(self,data, search_value):
        datalist = []
        for item in data:
            if search_value.upper() in item[self.tablevalues[0]].upper():
                print(item[self.tablevalues[0]])
                datalist.append(item)
        return datalist

class MenuHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.sortingmethods = ["name","price"]
        self.tablevalues = ['title','price']

class UsersHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.sortingmethods = ["name","email"]
        self.tablevalues = ['id',"cart","name", "email", "gender", "password", 'points', 'reward']
        self.adminvalues = ['id',"name", "email", "gender", "password"]
        self.currentuser = {}
    def signup(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM USERS")
        totalusers = len(cur.fetchall())

        data = [ totalusers + 1,"",user["name"], user["email"], user["gender"], user["password"], 0, 0, "", ""]
        cur.execute("INSERT INTO USERS (id, cart, name, email, gender, password, points, reward, card_details, favourite) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        connect.commit() 
        connect.close()
        return 0
    def login(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        userfromdb = {}
        print("Logging in...")
        employee_check = False
        try:
            cur.execute(f"SELECT * FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()
            if usertemp is not None:
                userfromdb = {self.tablevalues[0]: usertemp[0], self.tablevalues[1] : usertemp[1], self.tablevalues[2] : usertemp[2], self.tablevalues[3] : usertemp[3], self.tablevalues[4] : usertemp[4], self.tablevalues[5] : usertemp[5], self.tablevalues[6] : usertemp[6], self.tablevalues[7] : usertemp[7]}
                print(userfromdb)
                admin_check = False
                cur.execute(f"Select * From Employees WHERE email = '{user['email']}'")
                usertemp = cur.fetchone()
                if usertemp is not None:
                    print('THIS USER IS AN EMPLOYEE')
                    employee_check = True
                else:
                    print("THIS USER IS NOT AN EMPLOYEE")

            if usertemp is None: # Makes it so no error will happen if email isnt in USER database.
                print('Invalid login details')
                cur.execute(f"Select * From ADMINS WHERE email ='{user['email']}'")
                usertemp = cur.fetchone()
                if usertemp is not None:
                    userfromdb = {self.tablevalues[0]: usertemp[0], self.tablevalues[1] : usertemp[1], self.tablevalues[2] : usertemp[2], self.tablevalues[3] : usertemp[3], self.tablevalues[4] : usertemp[4], self.tablevalues[5] : usertemp[5]}
                    print(userfromdb)
                    admin_check = True

                else:
                    print('Invalid Admin and user login')
                    admin_check = False
                
          

        except(IOError):
            print("error occurance")
            print(IOError)
        
        if 'password' in userfromdb and userfromdb['password'] == user['password']: # This makes it so no error if wrong password is input.
            print("Login Success")
            self.currentuser = userfromdb
            return True, admin_check, employee_check
        else:
            print("Login Fail")
            return False, admin_check, employee_check
    def parcecart(self, cart):
        lis = []
        print("\nUnparced cart:\n",cart)
         
        if cart is None: # Stops error incase there is empty cart
            return lis  
        if cart == "":
            return lis
        cleanstr = cart.strip('|')
        cleanstr = cleanstr.strip(',')
        cleanstr = cleanstr.strip('|')
        items = cleanstr.split('|')
        print("\nITEMS:")
        for item in items:
            print(item)
            cleanitem = item.strip(',')
            values = cleanitem.split(',')
            print('values before error',values)
            for value in values:
                print("VALUE:\n",value)
            lis.append({"title":values[0], "size":values[1],"quantity":values[2], 'img_url':values[3], 'price':float(values[4])})
        counter =0
        for lisitems in lis:
            counter += 1
            print("listitem:",lisitems)
        return lis
    
    def compresscart(self, cart): ### this function compresses cart from dict to string format
        compressedstr = ""
        for item in cart:
            compressedstr = compressedstr + f"{item['title']},{item['size']},{item['quantity']},{item['img_url']},{item['price']}|,"
        print("Compressedcart:\n",compressedstr)
        return compressedstr
            

    def addtocart(self, user, product_id, reward_price = None, normal_price = None): # make this append data to user database
        if self.login(user)[0] == True:
            quantity_placeholder = 1
            size_placeholder = "s"
            connect = sqlite3.connect('database.db') 
            cur = connect.cursor()
            cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()
         #   print(usertemp)
            current_cart = usertemp[0] if usertemp[0] is not None else ""  ### user temp is a tuple for some reason so this is how it is
            
            end_strip_cart = current_cart.rstrip('|')
            strip_cart = end_strip_cart.split('|')
            cart_list = [item.split(',') for item in strip_cart]
            discount_item = sqlite_functions.select_from_table('Discounts')
            print(discount_item[0]['ID'])
        
          
      
            if product_id['title'] in current_cart: # This if statement allows products to have more than 1. Adjusts the price and quantity for the specific coffee
             
                fixed_cart_list = [[item for item in product if item] for product in cart_list]
                print('clean list:', fixed_cart_list)
                for cart in fixed_cart_list:
                    if product_id['title'] == cart[0]:
                        old_number = (int(cart[2]))
                        if reward_price == 2:
                            new_number = old_number + 2
                        else: 
                            new_number = old_number + 1
                        string_number = (str(new_number))
                        cart[2] = string_number
                        print(cart[4])
                        old_price = (float(cart[4]))
                        if discount_item[0]['ID'] == product_id['id'] and reward_price != 1:
                    
                            discount_price = (product_id['price'] * 50) / 100
                            new_price = old_price + discount_price
                        elif reward_price == 1:
                            new_price = old_price
                        elif reward_price == 3 and discount_item[0]['ID'] != product_id['id']:
                          
                            discount_price = (product_id['price'] * 90) / 100
                            new_price = old_price + discount_price
                        else:
                            new_price = old_price + product_id['price'] 
                        new_price = round(new_price, 2)    
                        string_price = (str(new_price))
                        cart[4] = string_price
                        updated_cart = [','.join(item) for item in fixed_cart_list]   
                        current_cart = '|'.join(updated_cart) + '|'
                        
               
            else: # This activates for products not in the cart. It picks the specific one depending on what reward the user has or if they have no rewards that manipulate the price
        
                if discount_item[0]['ID'] == product_id['id'] and reward_price != 1: # If user bought item of the day product
                    print('discountttttttttttttttttt')
                    discount_number = (product_id['price'] * 50) / 100
                    print(discount_number)
                    newitem = f"{product_id['title']},{size_placeholder},{quantity_placeholder},{product_id['img_url']},{round(discount_number, 2)}|"
                
                elif reward_price == 1: # user bought free coffee reward- this is why price  placeholder is zero
                    newitem = f"{product_id['title']},{size_placeholder},{quantity_placeholder},{product_id['img_url']},{0}|"
                
                elif reward_price == 2: # user bought  buy one get 1 free - This is why quantity is 2.
                    newitem = f"{product_id['title']},{size_placeholder},{2},{product_id['img_url']},{product_id['price']}|"
                
                elif reward_price == 3:  
                    discount_number = (product_id['price'] * 90) / 100
                    newitem = f"{product_id['title']},{size_placeholder},{quantity_placeholder},{product_id['img_url']},{round(discount_number, 2)}|"
 
                else: # USER has no reward that manipulates the price.
                    newitem = f"{product_id['title']},{size_placeholder},{quantity_placeholder},{product_id['img_url']},{product_id['price']}|"
              #  print("NEW ITEM\n",newitem)
                current_cart = current_cart + newitem
          #  print("ProductID:\n",product_id['title'])
        #    print("current cart:\n",current_cart['gender'])
        
        
            
            val = (str(current_cart),user["email"])
            command = (f"UPDATE USERS SET cart = '{val[0]}' WHERE email = '{val[1]}'")
            cur.execute(command)
            connect.commit()
            connect.close()
            return 0
        

    def removefromcart(self,user,product_id):
        if self.login(user)[0] == True:
            connect = sqlite3.connect('database.db') 
            cur = connect.cursor()
            cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()

            current_cart = usertemp[0] if usertemp[0] is not None else ""  ### user temp is a tuple for some reason so this is how it is, in string form
        
            if product_id not in current_cart:
                return "Already not in cart ERROR, function to add more needed"

            for item in user['cart']:
                if product_id == item["title"]:
                    print("REMOVING ITEM:", item)
                    user["cart"].remove(item)
            
            compressedcart = self.compresscart(user["cart"])
            
            val = (str(compressedcart),user["email"])
            command = (f"UPDATE USERS SET cart = '{val[0]}' WHERE email = '{val[1]}'")
            cur.execute(command)
            connect.commit()
            connect.close()
            return 0
    def updateusr(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
        usertemp = cur.fetchone()
        connect.close()
        if usertemp is None:
            print("User not found in database.")
            return None  
        freshuser = user
        print('freshuser is:', freshuser)
        print(usertemp)
        freshuser['cart'] = self.parcecart(usertemp[0])
        print('check again is:', freshuser)
        return freshuser

    

     