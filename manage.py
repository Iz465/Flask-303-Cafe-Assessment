from flask import Flask, redirect, url_for, request, render_template, flash, session
from forms import SignUpForm, Login, EmployForm, AddProductForm, AddRewardForm, AddJobForm, CheckOutForm
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
        session['loggedin'] = None
        session['admin_check'] = None
        session['employee_check'] = None
    num += 1
    print('employee right now is:',session['employee_check'])

@app.context_processor # Add things here that will be used in Jinga. This way you dont have to do it for every render template. This app will do it for every render template instead
def context_processor():
    loggedin = session['loggedin']
    admin_check = session['admin_check']
    employee_check = session['employee_check']
    currentuser = session['currentuser'],
    
    return dict(loggedin=loggedin, employee_check = employee_check, admin_check = admin_check, currentuser = currentuser)


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
        session['employee_check'] = None
        session['loggedin'] = False
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
            login_check, admin_check, employee_check = userhandler.login(form.data)
            if login_check: 
                session['currentuser'] = userhandler.currentuser # Storing user info in here so it can be accessed in other pages.
                currentuser = session['currentuser']
                print(currentuser)
                print('admin check is : ', admin_check)
                session['admin_check'] = admin_check
                if admin_check is False:
                    currentuser = userhandler.updateusr(currentuser)
                if employee_check is True:
                    session['employee_check'] = True
                else:
                    session['employee_check'] = False
                session['loggedin'] = True
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
            sqlite_functions.insert_into_table('Discounts', ['ID', 'Name', 'Contains', 'Description', 'Price', 'Image_Url', 'Time_Added'],
                                               (product[0], product[1], product[2], product[3], product[4], product[5], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
    return render_template('rewards-index.html', rows = rows)

### EMPLOY PAGE OPERANDS ###
@app.route('/employ')
def employ():
    if request.method == 'POST':
        return redirect(url_for('welcome-index'))
    
    rows = sqlite_functions.get_table('EmployJobs') # Make images 3000 height and 2000 width
    return render_template('employ-index.html', rows = rows)


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
                    return render_template('employ_application.html', form = form, check_form = False, form_done = True)
                else:
                    return render_template('employ_application.html', already_applied = True)
        else:
            return render_template('employ_application.html', form = form, check_form = True)
    else:
        return render_template('employ_application.html', notloggedin = True)


@app.route('/application_review', methods = ['POST', 'GET'])
def application_review():
    add_product = add_reward = add_job = False
    product_form = AddProductForm()
    reward_form = AddRewardForm()
    job_form = AddJobForm()
    
    form_values = request.form.keys()
    form_values = { 'Approve': more_functions.approve, 'Deny': more_functions.deny, 'add_product': more_functions.add_item, 'remove_product': more_functions.remove_item,
                   'add_reward': more_functions.add_item, 'remove_reward': more_functions.remove_item, 'add_job': more_functions.add_item, 
                   'remove_job': more_functions.remove_item, 'remove_employee': more_functions.remove_item } # Holding the request names in dictionary so i can make the code cleaner
    if request.method == 'POST':
       for form_action, function in form_values.items():
         if form_action in request.form:
                id = request.form.get(form_action) 
                if form_action in ['Approve', 'Deny']:
                    function(id) # activates the function from the form values dictionary
                elif 'add' in form_action:
                   if 'product' in form_action:
                       add_product = function() 
                   elif 'reward' in form_action:
                       add_reward = function() 
                   elif 'job' in form_action:
                       add_job = function()  

                elif 'remove_' in form_action:
                    function('MENU' if 'product' in form_action else 'Rewards' if 'reward' in form_action else 'EmployJobs' if 'job' in form_action else 'Employees', id)
                else:
                    function()
                break   # will stop loop once the action value being used in form is found
         
       if product_form.validate():
           print("Product added")
           sqlite_functions.insert_into_table('testing_table', ['product', 'price', 'ingredients', 'image', 'description'],
                                              (product_form.product.data, product_form.price.data, product_form.ingredients.data, product_form.image.data, product_form.description.data))
       if reward_form.validate():
           print("Reward added")
           sqlite_functions.insert_into_table('Rewards', ['Name', 'Points', 'Image_Url'],
                                              (reward_form.reward.data, reward_form.points.data, reward_form.image.data))
       if job_form.validate():
           print('Job added')
           sqlite_functions.insert_into_table('EmployJobs', ['Job_Name', 'Salary', 'Description', 'Image_Url'],
                                              (job_form.job.data, job_form.salary.data, job_form.description.data, job_form.image.data))
           
    db_tables = ['Employ_Application', 'Rewards', 'MENU', 'EmployJobs', 'Employees']
    rows = {table: sqlite_functions.get_table(table) for table in db_tables}
    return render_template('review_application.html',  product_form = product_form, reward_form = reward_form, job_form = job_form, add_job = add_job, add_reward = add_reward, 
                           add_product = add_product, employee_rows = rows['Employees'], job_review_rows = rows['Employ_Application'], rewards_rows = rows['Rewards'], 
                           products_rows = rows['MENU'], job_rows = rows['EmployJobs'])


@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    form = CheckOutForm()
    if request.method == 'POST':
        cart_sum = request.form['cart_sum']
        cart_length = request.form['cart_length']
        return render_template('checkout.html', form = form, cart_sum = cart_sum, cart_length = cart_length)
    return render_template('checkout.html', form = form)

        



if __name__ == '__main__':
    app.run(debug=True)


   

