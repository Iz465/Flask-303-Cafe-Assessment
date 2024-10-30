from flask import Flask, redirect, url_for, request, render_template, flash, session
from forms import SignUpForm, Login, EmployForm, AddProductForm
import sqlite3
import random
from datetime import datetime, timedelta
import sqlite_functions, more_functions

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
    #    product = sqlite_functions.select_from_table('MENU', category='id', value=(random.randrange(min_id,max_id + 1),))
    timeleft = None
    timeleft_converted = 0
    if product is not None: # checks whether there is a product with that id.
        empty_check = sqlite_functions.select_from_table('Discounts')
        if len(empty_check) < 1: # using this so only one product can be put in discount table
            discount_product = sqlite_functions.select_from_table('Discounts', category='ID', value=product[0])
            if discount_product is None: # checks whether that specific menu product is in the discount table.
                sqlite_functions.insert_into_table('Discounts', ['ID', 'Name', 'Contains', 'Description', 'Price', 'Image_Url', 'Time_Added'],
                                                   (product[0], product[1], product[2], product[3], product[4], product[5], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
            
    rows = sqlite_functions.get_table('Discounts')
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

### Experimental Map stuff
@app.route('/map', methods=["GET", "POST"])
def map():
    if request.method == "POST":
        post = True
      # The code here determines what happens after sumbitting the form
    else:
        # Render the input form
        post = False
        return render_template('map.html')
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
    if 'loggedin' in session and session['loggedin']:  # This if statement will check first, whether session has loggedin and then if the loggedin value is set to true. Only logged in users can access this.  
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
    form_values = request.form.keys()
    form_values = { 'Approve': more_functions.approve, 'Deny': more_functions.deny, 'add_product': more_functions.add_product, 'remove_product': more_functions.remove_product } # Holding the request names in dictionary so i can make the code cleaner
    if request.method == 'POST':
       for form_action, function in form_values.items():
         if form_action in request.form:
                if form_action in ['Approve', 'Deny']:
                    id = request.form.get(form_action) 
                    function(id) # activates the function from the form values dictionary
                elif form_action in ['add_product']:
                    add_product = function()
                else:
                    function()
                break  # will stop loop once the action value being used in form is found
         
       if form.validate():
        print("added product values:",form.product.data)
        sqlite_functions.insert_into_table('testing_table', ['product', 'price', 'ingredients', 'image', 'description'],
                                           (form.product.data, form.price.data, form.ingredients.data, form.image.data, form.description.data))
       else:
        print('Product not valid')

    db_tables = ['Employ_Application', 'Rewards', 'MENU', 'EmployJobs', 'Employees']
    rows = {table: sqlite_functions.get_table(table) for table in db_tables}
    return render_template('review_application.html',  form = form, add_product = add_product, employee_rows = rows['Employees'], job_review_rows = rows['Employ_Application'], rewards_rows = rows['Rewards'], products_rows = rows['MENU'], job_rows = rows['EmployJobs'], currentuser = session["currentuser"])
        



if __name__ == '__main__':
    app.run(debug=True)


   

