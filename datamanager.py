
import sqlite3 
import os, sys, json

connect = sqlite3.connect('database.db') 
cur = connect.cursor()
class DatabaseManager:
    def __init__(self):
        self.data = []
        self.deletetable_execute = "" ### "DROP TABLE <tablename>"
        self.createtable_execute = "" ### replace this with something like: CREATE TABLE IF NOT EXISTS <tablename>(title TEXT, description TEXT, price REAL, img_url TEXT)
        self.insertitems_execute = "" ### amount of ? determines number of keys in table
        self.getitems_excecute = "" ### "SELECT title, description, price FROM <tablename>"
        self.commonfunc = [self.show_tables.__name__,self.show_values.__name__, self.newitem.__name__,self.importjson.__name__]

    def show_tables(self):
        res = cur.execute("SELECT name FROM sqlite_master")
        tableslist = res.fetchall()
        print(len(tableslist))
        for table in tableslist:
            print(table)
    
    def newitem(self):
        data = []
        for key in self.data:
            value = input(f"{key}: ")
            data.append(value)
        cur.execute(self.insertitems_execute, data)
        connect.commit() 
    
    def importjson(self,jsondict):
        return 0

    def show_values(self):
        res = cur.execute(self.getitems_excecute)
        itemlist = res.fetchall()
        for item in itemlist:
            print(item)
    

class Menu(DatabaseManager):
    def __init__(self):
        super().__init__()
        cur.execute("CREATE TABLE IF NOT EXISTS MENU(id INT, title TEXT, contains TEXT, description TEXT, price REAL, img_url TEXT)")
        self.deletetable_execute = "DROP TABLE MENU"
        self.data = ["id","title", "contains", "description", "price", "Img url"]
        self.insertitems_execute = "INSERT INTO MENU VALUES(?, ?, ?, ?, ?, ?)"
        self.getitems_excecute = "SELECT title, description, price FROM MENU"
    
    def importjson(self,jsondict):
        connect.execute(self.deletetable_execute) 
        connect.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS MENU(id INT, title TEXT, contains TEXT, description TEXT, price REAL, img_url TEXT)")
        data = []
        for item in jsondict['item']:
            data.append([item["id"],item["title"],item["cont"],item["description"],item["price"],item["img_url"]]) #case sensative
        for d in data:
            print (d)
            
        cur.executemany(self.insertitems_execute, data)
        connect.commit()
    

def managedatabases(obj):
    count = 0
    for i in obj.commonfunc:
        count += 1
        print(f"{count}: {i}")
    ans = input("input: ")
    if ans == "1":
        obj.show_tables()
    if ans == "2":
        obj.show_values()
    if ans == "3":
        obj.newitem()
    if ans == "4":
        obj.importjson(parcejson())
    
    




def adminmenu():
    x = input("Input: ")
    if x == "1":
        menumanager = Menu()
        managedatabases(menumanager)
    if x == "2":
        j = parcejson()
        print(j.items())



def main():
    print("select option \n1: Menu manager\n2: Read Json ")
    adminmenu()
    connect.close()

def parcejson():
    try:
        with open("static\data\data.json","r") as f:
            print("Reading file")
            jsondict = json.load(f)
            return jsondict
    except(IOError):
        print(IOError)

if __name__ == '__main__': 
    main()