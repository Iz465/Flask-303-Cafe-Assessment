
import sqlite3 
import os, sys

connect = sqlite3.connect('database.db') 
cur = connect.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS MENU(title TEXT, description TEXT, price TEXT, img_url TEXT)") 

class Menuitem:
  def __init__(self):
    self.title = input("title: ")
    self.desc = input("description: ")
    self.price = input("price: ")
    self.img_url = input("Img url: ")

def printtables():
    res = cur.execute("SELECT name FROM sqlite_master")
    return res.fetchall()
def printvalues():
    print("Printing:")
    res = cur.execute("SELECT title, description FROM MENU")
    itemlist = res.fetchall()
    for item in itemlist:
        print(item)
def join(itemlist):
    data = []
    for item in itemlist:
        data.append([item.title,item.desc,item.price,item.img_url])
        print(item.title)
    
    cur.executemany("INSERT INTO MENU VALUES(?, ?, ?, ?)", data)
    connect.commit()   



def adminmenu():
    ans = input("Input: ")
    if ans == "1":
        itemlist = []
        item = Menuitem()
        itemlist.append(item)
        join(itemlist)
    if ans == "2":
        printvalues()


def main():
    print("select option \n1: all database tables:")
    adminmenu()
    fetch = printtables()
    for i in fetch:
        print(i)
    connect.close()

if __name__ == '__main__': 
    main()