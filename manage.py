from flask import Flask, redirect, url_for, request, render_template
import sqlite3
import menuhandler
from forms import EmployForm

app = Flask(__name__)
connect = sqlite3.connect('database.db')


def getdb_dict():
        connect.row_factory = sqlite3.Row
        values = connect.execute("SELECT * FROM MENU").fetchall()
        connect.close()
        list_accumulator = []
        for item in values:
            list_accumulator.append({k: item[k] for k in item.keys()})
        return list_accumulator

database_menu = getdb_dict()

### ROUTE TO HOME PAGE ###
@app.route('/')
def index():
    return render_template('welcome-index.html')

### ROUTE TO ADMIN
@app.route('/admin')
def hello_admin():
    return "hello Admin"

### HOME PAGE OPERANDS ###
@app.route('/home')
def home():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))
                                                  
 #   connect = sqlite3.connect('database.db')
 #   cursor = connect.cursor()
 #   cursor.execute("Select * FROM MENU WHERE id = ?", (5,))
 #   product = cursor.fetchone()

 #   if product is None:
 #       add_product = "Insert INTO Discounts (ID, Name, Contains, Description, Price, Image_Url) Values (?,?,?,?,?,?)"
 #       cursor.execute(add_product, (product[0], product[1], product[2], product[3], product[4], product[5]))
 #       connect.commit()
       

    return render_template('welcome-index.html')



### MENU PAGES OPERANDS ###
@app.route('/menu', methods=["POST","GET"])
def menu():
    data_dict = []
    handler = menuhandler.MenuHandler()
    if request.method == 'POST':
        searchbyvalue = request.form.get("search")
        sortbyvalue = request.form.get("sortdropdown")
        if len(searchbyvalue) > 0:
            data_dict = handler.searchdata(database_menu,searchbyvalue)
            print("GRATER THAN 0")
            data_dict = handler.sorteddata(data_dict,sortbyvalue)
        else:
            data_dict = handler.sorteddata(database_menu,sortbyvalue)

        return render_template('menu-index.html', sortbyvalue = sortbyvalue, searchbyvalue = searchbyvalue, data=data_dict)

    # show the form, it wasn't submitted
    print("Rendr: Default")
    return render_template('menu-index.html', data = database_menu)

@app.route('/<int:product_id>', methods=["POST","GET"])
def product(product_id):
    product_item = {}
    for product in database_menu:
        if product['id'] == product_id:
            product_item = product
    
    return render_template("product-index.html", product = product_item)


### REWARDS PAGE OPERANDS
@app.route('/rewards')
def rewards():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("select * from Rewards")
    rows = cur.fetchall()
    return render_template('rewards-index.html', rows = rows)

### EMPLOY PAGE OPERANDS ###
@app.route('/employ')
def employ():
    if request.method == 'POST':
     
        return redirect(url_for('welcome-index'))

  
    connect = sqlite3.connect('database.db') #make images 3000 height and 2000 width
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("select * from EmployJobs")
    rows = cur.fetchall()
    return render_template('employ-index.html', rows = rows)


if __name__ == '__main__':
    app.run(debug=True)