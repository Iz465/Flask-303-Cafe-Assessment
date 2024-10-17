
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
        self.tablevalues = ['id',"cart","name", "email", "gender", "password"]
        self.currentuser = {}
    def signup(self,user):
        connect = sqlite3.connect('database.db') 
        cur = connect.cursor()
        data = [ user["name"], user["email"], user["gender"], user["password"]]
        cur.execute("INSERT INTO USERS (name, email, gender, password) VALUES (?, ?, ?, ?)", data)
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
                userfromdb = {self.tablevalues[0]: usertemp[0], self.tablevalues[1] : usertemp[1], self.tablevalues[2] : usertemp[2], self.tablevalues[3] : usertemp[3], self.tablevalues[4] : usertemp[4], self.tablevalues[5] : usertemp[5]}
                print(userfromdb)
        except(IOError):
            print("error occurance")
            print(IOError)
        
        if 'password' in userfromdb and userfromdb['password'] == user['password']: # This makes it so no error if wrong password is input.
            print("Login Success")
            self.currentuser = userfromdb
            return True
        else:
            print("Login Fail")
            return False
    