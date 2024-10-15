from flask import Flask, redirect, url_for, request, render_template, flash
from forms import SignUpForm, Login
import sqlite3
import random
from forms import EmployForm
from datetime import datetime, timedelta
from datahandler import MenuHandler, UsersHandler

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

from flask_bcrypt import Bcrypt

from flask_login import LoginManager



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Using SQLite as the database 
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


app.secret_key = "Dev Key"
connect = sqlite3.connect('database.db')

class User(UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

def getmenu_dict():
        connect.row_factory = sqlite3.Row
        values = connect.execute("SELECT * FROM MENU").fetchall()
        connect.close()
        list_accumulator = []
        for item in values:
            list_accumulator.append({k: item[k] for k in item.keys()})
        return list_accumulator
def getusers_dict():
        connect.row_factory = sqlite3.Row
        values = connect.execute("SELECT * FROM USERS").fetchall()
        connect.close()
        list_accumulator = []
        for item in values:
            list_accumulator.append({k: item[k] for k in item.keys()})
        return list_accumulator

database_menu = getmenu_dict()

### ROUTE TO HOME PAGE ###
@app.route('/')
def index():
    return redirect(url_for('home'))

### ROUTE TO ADMIN
@app.route('/admin')
def hello_admin():
    return "hello Admin"

### LOGIN OPERANDS
@app.route('/login',methods=['GET','POST'])
def login():
    form = Login(request.form)
    userhandler = UsersHandler()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All Fields Required')
            return render_template('login.html', form = form)
        else:
            if userhandler.login(form.data) == True:
                currentuser = userhandler.currentuser
                print(currentuser)
                return render_template('profile.html', name = currentuser)
            return render_template('login.html', form = form)
    if request.method == 'GET':
        return render_template('login.html', form = form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignUpForm(request.form)
    userhandler = UsersHandler()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All Fields Required')
            print("error occurance")
            return render_template('signup.html', form = form)
        else:
            userhandler.signup(form.data)
            print('printing form:')
            print(form.data)
            return f'{form.name}\n{form.email}\n{form.gender}'
    if request.method == 'GET':
        print("getting form")
        return render_template('signup.html', form = form)

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
    timeleft = None
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
            else:
                print("Product is already in discount table")
        else:
            cursor.execute("SELECT * FROM Discounts")
            discount_product = cursor.fetchone()
            product_start_time = datetime.strptime(discount_product[6], '%Y-%m-%d %H:%M:%S')
            if datetime.now() > product_start_time + timedelta(days=1):
                cursor.execute("DELETE From Discounts") # this will delete all rows from Discounts database, allowing another product to be stored in it.
                connect.commit()
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
    handler = MenuHandler()
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
    with app.app_context():
        db.create_all()

    app.run(debug=True)