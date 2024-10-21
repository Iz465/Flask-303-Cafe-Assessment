
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
        self.tablevalues = ["cart","name", "email", "gender", "password"]
        self.currentuser = {}
    def signup(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        data = ["", user["name"], user["email"], user["gender"], user["password"]]
        cur.execute("INSERT INTO USERS (cart, name, email, gender, password) VALUES (?, ?, ?, ?, ?)", data)
        connect.commit() 
        connect.close()
        return 0
    def login(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        userfromdb = {}
        print("Logging in...")
        try:
            cur.execute(f"SELECT * FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()
            if usertemp is None: # Makes it so no error will happen if email isnt in USER database.
                print('Invalid login details')
            else:
                print(self.tablevalues)
                print(usertemp)
                userfromdb = {self.tablevalues[0]: usertemp[0], self.tablevalues[1] : usertemp[1], self.tablevalues[2] : usertemp[2], self.tablevalues[3] : usertemp[3], self.tablevalues[4] : usertemp[4]}
                print(userfromdb)
        except(IOError):
            print("error occurance")
            print(IOError)
        
        connect.close()
        if 'password' in userfromdb and userfromdb['password'] == user['password']: # This makes it so no error if wrong password is input.
            print("Login Success")
            self.currentuser = userfromdb
            self.currentuser['cart'] = self.parcecart(userfromdb["cart"])
            return True
        else:
            print("Login Fail")
            return False
    def parcecart(self, cart):
        lis = []
        print(cart)
        if cart == "":
            return lis
        print("CART:",cart)
        cleanstr = cart.rstrip('|')
        cleanstr = cleanstr.rstrip(',')
        cleanstr = cleanstr.rstrip('|')
        items = cleanstr.split('|')
        print("ITEMS:",items)
        for item in items:
            values = item.split(',')
            print(values)
            lis.append({"title":values[0], "size":values[1],"quantity":values[2], 'img_url':values[3]})
        counter =0
        for lisitems in lis:
            counter += 1
            print("listitem:",lisitems)
        return lis
    
    def compresscart(self, cart):
        compressedstr = ""
        for item in cart:
            compressedstr = compressedstr + f"{item['title']},{item['size']},{item['quantity']},{item['img_url']}|,"
        return compressedstr
            

    def addtocart(self, user, product_id): # make this append data to user database
        if self.login(user) == True:
            quantity_placeholder = 1
            size_placeholder = "s"
            connect = sqlite3.connect('database.db') 
            cur = connect.cursor()
            cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()
            print(usertemp)
            current_cart = usertemp[0] ### user temp is a tuple for some reason so this is how it is
            if product_id['title'] in current_cart:
                return "Already in cart, function to add more needed"

            newitem = f"{product_id['title']},{size_placeholder},{quantity_placeholder},{product_id['img_url']}|"

            current_cart = current_cart + newitem

            
            val = (str(current_cart),user["email"])
            command = (f"UPDATE USERS SET cart = '{val[0]}' WHERE email = '{val[1]}'")
            cur.execute(command)
            connect.commit()
            connect.close()
            return 0
    def removefromcart(self,user,product_id):
        if self.login(user) == True:
            connect = sqlite3.connect('database.db') 
            cur = connect.cursor()
            cur.execute(f"SELECT cart FROM USERS WHERE email ='{user['email']}'")
            usertemp = cur.fetchone()

            current_cart = usertemp[0] ### user temp is a tuple for some reason so this is how it is, in string form
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
        freshuser = user
        freshuser['cart'] = self.parcecart(usertemp[0])
        return freshuser

    