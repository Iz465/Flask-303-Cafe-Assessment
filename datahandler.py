
from operator import itemgetter
import sqlite3

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
        self.tablevalues = ['id',"cart","name", "email", "gender", "password", 'points']
        self.adminvalues = ['id',"name", "email", "gender", "password"]
        self.currentuser = {}
    def signup(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM USERS")
        totalusers = len(cur.fetchall())

        data = [ totalusers + 1,"",user["name"], user["email"], user["gender"], user["password"], 0]
        cur.execute("INSERT INTO USERS (id, cart, name, email, gender, password, points) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
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
                print(self.tablevalues)
                print(usertemp)
                userfromdb = {self.tablevalues[0]: usertemp[0], self.tablevalues[1] : usertemp[1], self.tablevalues[2] : usertemp[2], self.tablevalues[3] : usertemp[3], self.tablevalues[4] : usertemp[4], self.tablevalues[5] : usertemp[5], self.tablevalues[6] : usertemp[6]}
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
        print("\nITEMS:", items[0])
        for item in items:
            cleanitem = item.strip(',')
            values = cleanitem.split(',')
            lis.append({"title":values[0], "size":values[1],"quantity":values[2], 'img_url':values[3], 'price':float(values[4])})
        
        print("Parced cart:")
        counter =0
        for lisitems in lis:
            counter += 1
            print("cart item:",counter)
            for item in lisitems.items():
                print(f"| {item[0]}: {item[1]}")
        return lis
    
    def compresscart(self, cart): ### this function compresses cart from dict to string format
        compressedstr = ""
        for item in cart:
            compressedstr = compressedstr + f"{item['title']},{item['size']},{item['quantity']},{item['img_url']},{item['price']}|,"
        print("Compressedcart:\n",compressedstr)
        return compressedstr
            

    def addtocart(self, user, product_id, size): # make this append data to user database
        if self.login(user)[0] == True:
            quantity_placeholder = 1
            size_char = size[0]
            connect = sqlite3.connect('database.db') 
            cur = connect.cursor()
            cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()
            print(usertemp)
            current_cart = usertemp[0] if usertemp[0] is not None else ""  ### user temp is a tuple for some reason so this is how it is

            if product_id['title'] in current_cart:
                return "Already in cart, function to add more needed"
            print("ProductID:\n",product_id['title'])
            print("current cart:\n",current_cart)
            
            newitem = f"{product_id['title']},{size_char},{quantity_placeholder},{product_id['img_url']},{product_id['price']}|"
            print("NEW ITEM\n",newitem)
            current_cart = current_cart + newitem

            
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
        freshuser['cart'] = self.parcecart(usertemp[0])
        return freshuser

    