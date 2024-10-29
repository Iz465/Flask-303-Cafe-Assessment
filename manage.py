from flask import Flask, redirect, url_for, request, render_template, flash, session
from forms import SignUpForm, Login, EmployForm, AddProductForm
import sqlite3
import random
from datetime import datetime, timedelta
import sqlite_functions

from datahandler import MenuHandler, UsersHandler



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Using SQLite as the database 


app.secret_key = "Dev Key"
connect = sqlite3.connect('database.db')

isloggedin= False
loggedin =[]
num = 0


@app.before_request # This happens everytime flask reloads, before the routes
def before_request():
    global num
    if num <1:
        session['currentuser'] = None
        session['currentuser'] = None
        session['admin_check'] = None
    num += 1

@app.context_processor
def context_processor():
    if 'currentuser' in session and session['currentuser'] is not None:
        print("member is logged in")
        session['loggedin'] = True
        loggedin = session['loggedin']
    else:
        session['loggedin'] = False
        loggedin = session['loggedin']
    if 'admin_check' in session and session['admin_check'] is not None:
        admin_check = session['admin_check']
        return dict(loggedin=loggedin, admin_check = admin_check)
    return dict(loggedin=loggedin)


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
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("logging out of user")
        session['currentuser'] = None
        session['admin_check'] = None
        return redirect(url_for('home'))
    print("not using logout post")
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
            login_check, admin_check = userhandler.login(form.data)
            if login_check: 
                session['currentuser'] = userhandler.currentuser # Storing user info in here so it can be accessed in other pages.
                currentuser = session['currentuser']
                print(currentuser)
                print('admin check is : ', admin_check)
                session['admin_check'] = admin_check
                if admin_check is False:
                    currentuser = userhandler.updateusr(currentuser)
                return render_template('profile.html', currentuser = currentuser)
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
            print("Errors:", form.errors)
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
                                                  
    connect = sqlite_functions.sqlite_connection()
    cursor = connect.cursor()
    
    cursor.execute("Select MIN(id), MAX(id) from MENU")
    min_id, max_id = cursor.fetchone()

    cursor.execute("Select * FROM MENU WHERE id = ?", (random.randrange(min_id,max_id + 1),))
    product = cursor.fetchone()
    timeleft = None
    timeleft_converted = 0
    if product is not None: # checks whether there is a product with that id.
        cursor.execute("Select * From Discounts")
        empty_check = cursor.fetchall()
        if len(empty_check) < 1: # using this so only one product can be put in discount table
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
    if timeleft is not None:
        timeleft_converted = int(timeleft.total_seconds()) 
    return render_template('welcome-index.html', currentuser = session['currentuser'], rows = rows, timeleft_converted = timeleft_converted)



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

        return render_template('menu-index.html', sortbyvalue = sortbyvalue, searchbyvalue = searchbyvalue, data=data_dict ,loggedin = session['loggedin'], currentuser = session["currentuser"])

    # show the form, it wasn't submitted
    print("Rendr: Default")
    return render_template('menu-index.html', data = database_menu, currentuser = session['currentuser'], loggedin = session['loggedin'])

@app.route('/<int:product_id>', methods=["POST","GET"])
def product(product_id):
    print(request.method)
    product_item = {}
    for product in database_menu:
        if product['id'] == product_id:
            product_item = product
    
    if request.method == "POST":
        usr = session["currentuser"]
        userhandler = UsersHandler()
        msg =userhandler.addtocart(usr,product_item)
        print(msg)
        print(usr)
        session["currentuser"] = userhandler.updateusr(usr)
        print("TYPE OF PRICE",session["currentuser"])
    return render_template("product-index.html", product = product_item, currentuser = session["currentuser"])

### Cart PAGE
@app.route('/cart', methods=["POST",'GET'])
def cart():
    cart_total = 0
    if session.get("currentuser"):
        for item in session["currentuser"]["cart"]:
            cart_total += item['price']
        if request.method == "POST":
            usr = session["currentuser"]
            userhandler = UsersHandler()
            item = request.form.get("removeitem")
            print("ITEM PRINTING:",item)
            msg =userhandler.removefromcart(usr,item)
            
            session["currentuser"] = userhandler.updateusr(usr)
    else:
        print('Log in to view your cart')
    return render_template('cart.html', currentuser = session["currentuser"],cart_total = cart_total)


### REWARDS PAGE OPERANDS
@app.route('/rewards')
def rewards():
    if request.method == 'POST':
        return redirect(url_for('welcome-index'))

    rows = sqlite_functions.get_table('Rewards')
    print('logged in is: ',session['loggedin'])
    return render_template('rewards-index.html', rows = rows, currentuser = session["currentuser"])

### EMPLOY PAGE OPERANDS ###
@app.route('/employ')
def employ():
    if request.method == 'POST':
        return redirect(url_for('welcome-index'))
    
    rows = sqlite_functions.get_table('EmployJobs') # Make images 3000 height and 2000 width
    return render_template('employ-index.html', rows = rows, currentuser = session["currentuser"])


@app.route('/employ_application', methods= ['POST', 'GET'])
def employ_application():
    form = EmployForm()
   # if request.method == 'POST':
      #  job_name = request.form['job_name']
       # print(job_name)
    if 'loggedin' in session and session['loggedin']:  # This if statement will check first, whether session has loggedin and then if the loggedin value is set to true. So only logged in users can access this.  
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('employ_application.html', form = form, check_form = True)
            else:
                connect = sqlite3.connect('database.db')
                cursor = connect.cursor()
                cursor.execute("Select id FROM Employ_Application")
                employ_ids = cursor.fetchall()
                check_users = [row[0] for row in employ_ids] # This adds the ids into the check users from the employ ids tuple, so they can be accessed individually.
                cursor.execute("Select id FROM Employees")
                employee_ids = cursor.fetchall()
                check_employees = [row[0] for row in employee_ids]
                if session['currentuser']['id'] not in check_users and session['currentuser']['id'] not in check_employees:
                    cursor.execute("Insert INTO Employ_Application (id, name, gender, job_reason) VALUES (?,?,?,?)", 
                    (session['currentuser']['id'],session['currentuser']['name'],session['currentuser']['gender'], request.form['job_reason'])) 
                    connect.commit()
                    connect.close() 
                    return render_template('employ_application.html', form = form, check_form = False, form_done = True, currentuser = session["currentuser"])
                else:
                    return render_template('employ_application.html', already_applied = True, currentuser = session["currentuser"])
        else:
            return render_template('employ_application.html', form = form, check_form = True, currentuser = session["currentuser"])
    else:
        return render_template('employ_application.html', notloggedin = True, currentuser = session["currentuser"])



@app.route('/application_review', methods = ['POST', 'GET'])
def application_review():
    add_product = False
    form = AddProductForm()
    if request.method == 'POST':
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        if 'Approve' in request.form:
            id = request.form.get('Approve')
            print("Approved Review")
            cursor.execute("SELECT id FROM USERS")
            employ_ids = cursor.fetchall()
            cursor.execute("SELECT * From USERS WHERE ID = ?", (id,))
            approved_user = cursor.fetchone()
            check_users = [row[0] for row in employ_ids]
            if id not in check_users:
                 cursor.execute("INSERT INTO Employees (ID, cart, name, email, gender, password) VALUES (?, ?, ?, ?, ?, ?)",
                 (approved_user[0], approved_user[1], approved_user[2], approved_user[3], approved_user[4], approved_user[5]))
                 cursor.execute("DELETE From Employ_Application WHERE ID = ?", (id,))
                 connect.commit()  
        elif 'Deny' in request.form:
            id = request.form.get('Deny')
            print("Denied Review")
            cursor.execute("DELETE From Employ_Application WHERE ID = ?", (id,))
            connect.commit()
        elif 'add_product' in request.form:
            add_product = True
        elif 'remove_product' in request.form:
            print('Deleting product from cafe')
        else:
            print("Not working")
        if form.validate() == False:
            print('Product not valid')
        else:
            print("added product values:",form.product.data)
            cursor.execute("INSERT INTO testing_table (product, price, ingredients, image, description) VALUES (?,?,?,?,?)",
                           (form.product.data, form.price.data, form.ingredients.data, form.image.data, form.description.data))
            connect.commit()
            connect.close()
    job_review_rows = sqlite_functions.get_table('Employ_Application')
    rewards_rows = sqlite_functions.get_table('Rewards')
    products_rows = sqlite_functions.get_table('MENU')
    job_rows = sqlite_functions.get_table('EmployJobs')
    employee_rows = sqlite_functions.get_table('Employees')
    return render_template('review_application.html',  form = form, add_product = add_product, employee_rows = employee_rows, job_review_rows = job_review_rows, rewards_rows = rewards_rows, products_rows = products_rows, job_rows = job_rows, currentuser = session["currentuser"])
        

if __name__ == '__main__':
    app.run(debug=True)


    #  <input id="product" name="product" required type="text" value="banana">