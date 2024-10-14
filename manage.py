from flask import Flask, redirect, url_for, request, render_template
import sqlite3
import menuhandler
import random
from forms import EmployForm
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'dfhdfhdfhdfh'
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
    return redirect(url_for('home'))

### ROUTE TO ADMIN
@app.route('/admin')
def hello_admin():
    return "hello Admin"

### HOME PAGE OPERANDS ###
@app.route('/home')
def home():
                                                  
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()
    

    cursor.execute("Select MIN(id), MAX(id) from MENU")
    min_id, max_id = cursor.fetchone()

    cursor.execute("Select * FROM MENU WHERE id = ?", (random.randrange(min_id,max_id + 1),))
    product = cursor.fetchone()

    timeleft = timedelta(0) 

    if product is not None: # checks whether there is a product with that id.
        cursor.execute("Select * From Discounts")
        empty_check = cursor.fetchall()
        print("length is",len(empty_check)) # using this so only one product can be put in discount table
        if len(empty_check) < 1:
            cursor.execute("SELECT * FROM Discounts WHERE ID = ?", (product[0],))
            discount_product = cursor.fetchone()
            if discount_product is None: # checks whether that specific menu product is in the discount table.
                add_product = "Insert INTO Discounts (ID, Name, Contains, Description, Price, Image_Url, Time_Added) Values (?,?,?,?,?,?,?)"
                cursor.execute(add_product, (product[0], product[1], product[2], product[3], product[4], product[5], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                connect.commit()
                print("Product is added to discount table")
                timeleft = timedelta(days=1)
            else:
                print("Product is already in discount table")
        else:
            cursor.execute("SELECT * FROM Discounts")
            discount_product = cursor.fetchone()
            product_start_time = datetime.strptime(discount_product[6], '%Y-%m-%d %H:%M:%S')
            if datetime.now() > product_start_time + timedelta(days=1):
                cursor.execute("DELETE From Discounts") # this will delete all rows from Discounts database, allowing another product to be stored in it.
                connect.commit()
                return redirect(url_for('home'))
            else:
                now = datetime.now()
                timeleft = timedelta(days=1) - (now -  product_start_time) 
                print(f"Product still has {timeleft} time left") 
            
    cursor.execute("SELECT * FROM Discounts") 
    rows = cursor.fetchall()
    connect.close()
    timeleft_converted = int(timeleft.total_seconds()) 
    return render_template('welcome-index.html', rows = rows, timeleft_converted = timeleft_converted)



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


@app.route('/employ-application', methods = ['POST', 'GET'])
def employ_application():
    form = EmployForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('employ_application.html', form = form)

    return render_template('employ_application.html', form = form)

if __name__ == '__main__':
    app.run(debug=True) 