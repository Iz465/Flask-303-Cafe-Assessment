from flask import Flask, redirect, url_for, request, render_template, flash, session
from forms import SignUpForm, Login, EmployForm, AddProductForm, AddRewardForm, AddJobForm, CheckOutForm
import sqlite3
import random
import json
from datetime import datetime, timedelta
import sqlite_functions, more_functions

from datahandler import UsersHandler



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Using SQLite as the database 


app.secret_key = "Dev Key"
connect = sqlite3.connect('database.db')

isloggedin= False
loggedin =[]
num = 0


@app.before_request # This happens everytime flask reloads meaning all this will happen before the code in the routes
def before_request():
    global num
    if num <1:
        session['currentuser'] = None
        session['loggedin'] = None
        session['admin_check'] = None
        session['employee_check'] = None
    num += 1


@app.context_processor # Add things here that will be used in Jinga. This way you dont have to do it for every render template. This app will do it for every render template instead
def context_processor():
    loggedin = session['loggedin']
    admin_check = session['admin_check']
    employee_check = session['employee_check']
    currentuser = session['currentuser']

    
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

@app.route('/logout')
def logout():
    print("logging out of user")
    session['currentuser'] = None
    session['admin_check'] = None
    session['employee_check'] = None
    session['loggedin'] = False
    return redirect(url_for('home'))
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
                return redirect(url_for('home'))
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
            return redirect(url_for('login'))
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
    rows = sqlite_functions.get_table('MENU')
    new_data = []
    for d in database_menu:
        new_data.append(json.dumps(d))
    for new in new_data:
        print(new)
    
    newreward = []
    isemployee = False

    if session['currentuser'] is not None: # This makes it so only logged in useres can see this.
        isemployee = session['employee_check']
        updated_reward = sqlite_functions.select_from_table('USERS', 'reward', 'ID', session['currentuser']['id'] )
        session['currentuser']['reward'] = updated_reward[0]['reward']
        reward = session['currentuser']['reward']
        rewards_split = reward.split(',')
        rewards_int_list = [int(number) for number in rewards_split]
        for i in rewards_int_list:
            newreward.append(json.dumps(i))
            print("Reward:",i)
        
        favourite_check = True

    if request.method == 'POST':
        if request.form.get('action') == 'favourite_form': # Only form posts that have favourite_form in them will access this.
            favourite_string = ''
            for row in rows:
                quantity = request.form.get(row['title'])
                if quantity != '':
                    print(f"quantity for {row['title']} is: {quantity}")
                    print(f"price for {row['title']} is: {float(row['price']) * float(quantity)}")
                    total_price = float(row['price']) * float(quantity)
                    favourite_string = favourite_string + f"{row['title']},{quantity}, {round(total_price, 2)}|"
            
            print(favourite_string)
            sqlite_functions.update_table('USERS', 'favourite', 'ID', favourite_string, session['currentuser']['id'])
            return redirect(url_for('menu'))
        

        
        return render_template('menu-index.html', data=new_data ,loggedin = json.dumps(session['loggedin']), currentuser = json.dumps(session["currentuser"]),employee_check = json.dumps(isemployee), rewards_int_list = newreward, favourite_check = favourite_check ,rows = rows)

    # show the form, it wasn't submitted
    print("Rendr: Default")
    print(session['loggedin'])

    if  session['currentuser'] is not None:
        return render_template('menu-index.html', data = new_data, currentuser = json.dumps(session['currentuser']), loggedin = json.dumps(session['loggedin']), employee_check = json.dumps(isemployee), rewards_int_list = newreward, favourite_check = favourite_check, rows = rows)
    return render_template('menu-index.html', data = new_data, currentuser = json.dumps(session['currentuser']),rewards_int_list = newreward, loggedin = json.dumps(session['loggedin']),employee_check = json.dumps(isemployee), rows = rows)
  
   

@app.route('/<int:product_id>', methods=["POST","GET"])
def product(product_id):
    print(request.method)
    product_item = {}
 
    for product in database_menu:
        if product['id'] == product_id:
            product_item = product
    
    newreward = []
    isemployee = False
    if session['currentuser'] is not None:
        updated_reward = sqlite_functions.select_from_table('USERS', 'reward', 'ID', session['currentuser']['id'] )
        session['currentuser']['reward'] = updated_reward[0]['reward']
        reward = session['currentuser']['reward']
        rewards_split = reward.split(',')
        rewards_int_list = [int(number) for number in rewards_split]
        for i in rewards_int_list:
            newreward.append(json.dumps(i))
            print("Reward:",i)

        isemployee = session['employee_check']
            
    if request.method == "POST":
        if session['currentuser'] is not None:
            reward = sqlite_functions.select_from_table('USERS', 'Reward', 'ID', session['currentuser']['id'] )
            rewards_split = reward[0]['Reward'].split(',')
            rewards_int_list = sorted([int(reward) for reward in rewards_split])
        
        
            size = request.form.get('pick-size')
            if size is None:
                size = 'S'
            print("SIZE OF DRINK:\n",size)

            usr = session["currentuser"]
            userhandler = UsersHandler()
            msg =userhandler.addtocart(usr,product_item, size, reward_price= rewards_int_list[0], normal_price=product_item['price'])
            print('the msg is?', msg)
            print('the user is?', usr)
            session["currentuser"] = userhandler.updateusr(usr)
    
            if rewards_int_list[0] != 0: # This makes it so this if statement will only occur if user has rewards bought.
                permanent = sqlite_functions.select_from_table('Rewards', 'Permanent', 'ID', rewards_int_list[0])
                if permanent[0]['permanent'] == 'No':
                    rewards_int_list.remove(rewards_int_list[0])
                    rewards_string_list = ','.join([str(reward) for reward in rewards_int_list])
                    if rewards_int_list == []:
                        rewards_int_list.append(0) 
                        rewards_string_list = ','.join([str(reward) for reward in rewards_int_list])
                    sqlite_functions.update_table('Users', 'reward', 'ID', rewards_string_list, session['currentuser']['id'])
            print('rewards list again:', rewards_int_list) # Show every reward the user has.
        
    return render_template("product-index.html", product = product_item, currentuser = session["currentuser"],rewards_int_list = newreward, employee_check = json.dumps(isemployee))



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
    return render_template('cart.html', currentuser = session["currentuser"], cart_total = cart_total)


### experiment minesweeper minigame
@app.route("/minesweeper",methods=['GET'])
def minesweeper():
    return render_template('minesweeper.html')
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
@app.route('/rewards', methods = ['POST', 'GET'])
def rewards():
    if session['currentuser'] is not None: # doing this atm because of strange problem where session isnt updating properly

        updated_points = sqlite_functions.select_from_table('USERS', 'points', 'ID', session['currentuser']['id'])
        updated_reward = sqlite_functions.select_from_table('USERS', 'reward', 'ID', session['currentuser']['id'])
        session['currentuser']['points'] = updated_points[0]['points']
        session['currentuser']['reward'] = updated_reward[0]['reward']

        points = updated_points[0]['points']
        reward = updated_reward[0]['reward']
        rewards_split = reward.split(',')
        rewards_int_list = [int(number) for number in rewards_split]
        print(rewards_int_list)                         
    else:
        points = reward = rewards_split = rewards_int_list = None
    
    if request.method == 'POST': # This is for when users buy a reward. 

        reward_points = int(request.form['reward_points'])
        reward_id = int(request.form['reward_id'])
        points = session.get('currentuser', {}).get('points', 0)
        current_reward_id = session['currentuser']['reward']
        if current_reward_id == '0':
            all_rewards = str(reward_id)
        else:
            all_rewards = str(current_reward_id) + ',' + str(reward_id) 

        new_points = points - reward_points
        sqlite_functions.update_table('USERS', 'points', 'ID', new_points, session['currentuser']['id'], 'reward', all_rewards)
        session['currentuser']['points'] = new_points
        print('currentuser points are: ', session['currentuser']['points'])
        return redirect(url_for('rewards'))
    
    rows = sqlite_functions.get_table('Rewards')
    return render_template('rewards-index.html', rows = rows, points = points, rewards_int_list = rewards_int_list)


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

    if 'loggedin' in session and session['loggedin']:  # This if statement will check first, whether session has loggedin and then if the loggedin value is set to true. Only logged in users can access this.  
        if request.method == 'POST':
            if form.validate() == False:
                return render_template('employ_application.html', form = form, check_form = True)
            else:
                employ_ids = sqlite_functions.select_from_table('Employ_Application', 'id')
                check_users = [row[0] for row in employ_ids] 
                employee_ids = sqlite_functions.select_from_table('Employees', 'id')
                check_employees = [row[0] for row in employee_ids]
                if session['currentuser']['id'] not in check_users and session['currentuser']['id'] not in check_employees: # This makes it so only users who have not applied or are employyes can apply for a job.
                    sqlite_functions.insert_into_table('Employ_Application', ['id', 'name', 'gender', 'job_reason'], 
                                                       (session['currentuser']['id'],session['currentuser']['name'],session['currentuser']['gender'],request.form['job_reason']))
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
                    print('4')
                    function('MENU' if 'product' in form_action else 'Rewards' if 'reward' in form_action else 'EmployJobs' if 'job' in form_action else 'Employees', id)
                else:
                    print('5')
                    function()
                break   # will stop loop once the action value being used in form is found
         
       if product_form.validate():
           print("Product added")
           sqlite_functions.insert_into_table('MENU', ['title', 'price', 'contains', 'img_url', 'description'],
                                              (product_form.product.data, product_form.price.data, product_form.ingredients.data, product_form.image.data, product_form.description.data))
       elif reward_form.validate():
           print("Reward added")
           sqlite_functions.insert_into_table('Rewards', ['Name', 'Points', 'Image_Url'],
                                              (reward_form.reward.data, reward_form.points.data, reward_form.image.data))
       elif job_form.validate():
           print('Job added')
           sqlite_functions.insert_into_table('EmployJobs', ['Job_Name', 'Salary', 'Description', 'Image_Url'],
                                              (job_form.job.data, job_form.salary.data, job_form.description.data, job_form.image.data))
       else:
           print('not added')
           
    db_tables = ['Employ_Application', 'Rewards', 'MENU', 'EmployJobs', 'Employees']
    rows = {table: sqlite_functions.get_table(table) for table in db_tables}
    return render_template('review_application.html',  product_form = product_form, reward_form = reward_form, job_form = job_form, add_job = add_job, add_reward = add_reward, 
                           add_product = add_product, employee_rows = rows['Employees'], job_review_rows = rows['Employ_Application'], rewards_rows = rows['Rewards'], 
                           products_rows = rows['MENU'], job_rows = rows['EmployJobs'])



@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    form = CheckOutForm()
    checkout_complete = incorrect_details = favourited_order = False

    if request.method == 'POST':
         if request.form.get('favourited_order') == 'true': # Only posts that have favourited_order will access this 
             print('showing favourite order')
             checkout_complete = favourited_order = True
             rows = sqlite_functions.select_from_table('USERS',category='ID', value=session['currentuser']['id'] )
             row_list = [list(row) for row in rows]
             row_strip = row_list[0][9].strip('|')
             remove = '|'
             change = row_strip.replace(remove, ',')
             favourite_list = change.split(',')
             favourite_sum = 0
             for i in range(2, len(favourite_list), 3): 
                favourite_sum += float(favourite_list[i]) 
                 
             return render_template('checkout.html', form = form, checkout_complete = checkout_complete, favourited_order = favourited_order, rows = rows, favourite_list = favourite_list, favourite_sum = favourite_sum)

         if form.validate():
            card = request.form['card_number']
            expiry_date = request.form['expiry_date']
            cvc = request.form['cvc']
            save_card = request.form.get('save_card') == 'y'
            print(save_card)
            if save_card:
                card_details = card + ',' + expiry_date + ',' + cvc
                print(card_details)
                sqlite_functions.update_table('USERS', 'card_details', 'ID', card_details, session['currentuser']['id'])
            else:
                print('card not saved')

            checkout_complete = True
            user_points = sqlite_functions.select_from_table('USERS', 'points', 'ID', session['currentuser']['id'] )
            users_rewards = session["currentuser"]['reward']
            rewards_split = users_rewards.split(',')
            cart_check = session['currentuser']['cart']
            if isinstance(user_points[0]['points'], int): 
                if '6' in rewards_split:
                    sqlite_functions.update_table('USERS', 'cart', 'ID', "", session['currentuser']['id'], 'points', user_points[0]['points'] + 100 )    
                else:
                    sqlite_functions.update_table('USERS', 'cart', 'ID', "", session['currentuser']['id'], 'points', user_points[0]['points'] + 50 )    
            else:
                sqlite_functions.update_table('USERS', 'cart', 'ID', "", session['currentuser']['id'], 'points', 50 )  
                session["currentuser"]['points'] = 0
            userhandler = UsersHandler()
            session["currentuser"] = userhandler.updateusr(session["currentuser"])
     
            if '6' in rewards_split:
                session["currentuser"]['points'] += 100 
            else:
                session["currentuser"]['points'] += 50 
            
            cart_quantity = ''
            cart_price = ''
            cart_title = ''

            for cart in cart_check:
                if cart_title:  
                    cart_title = cart_title + ',' + cart['title']
                else:
                    cart_title = cart['title']
    
                if cart_quantity:  
                    cart_quantity = cart_quantity + ',' + cart['quantity']  # Convert to string if necessary
                else:
                    cart_quantity = cart['quantity']
    
                if cart_price:  
                    cart_price = cart_price + ',' + str(cart['price'])  # Convert to string if necessary
                else:
                    cart_price = str(cart['price'])


            titles = cart_title.split(',')
            quantities = cart_quantity.split(',')
            prices = cart_price.split(',')
            print('Final titles:', titles)
            print('Final quantities:', quantities)
            print('Final prices:', prices)
            cart_finished = list(zip(titles, quantities, prices))
            cart_sum = float(session['cart_sum'])
            return render_template("checkout.html", checkout_complete = checkout_complete, cart_finished = cart_finished, cart_sum = cart_sum)
         
         
         
         if form.validate() == False:
            incorrect_details = True
            cart_items = session['cart_items']
            cart_sum = session['cart_sum']
            cart_length = session['cart_length']
            return render_template("checkout.html", form = form, incorrect_details = incorrect_details, cart_sum = cart_sum, cart_length = cart_length, cart_items = cart_items)
    # GET PART BELOW
    cart_items = session.get('currentuser', {}).get('cart', "")
    session['cart_items'] = cart_items
    cart_sum = request.args.get('cart_sum', '0') 
    session['cart_sum'] = cart_sum
    cart_sum_int = (float(cart_sum))
   

    connect = sqlite3.connect('database.db') 
    cur = connect.cursor()
    cur.execute(f"SELECT cart FROM USERS WHERE email ='{session['currentuser']['email']}'")
    usertemp = cur.fetchone()
    current_cart = usertemp[0] if usertemp[0] is not None else ""          
    end_strip_cart = current_cart.rstrip('|')
    strip_cart = end_strip_cart.split('|')
    cart_list = [item.split(',') for item in strip_cart]
    fixed_cart_list = [[item for item in product if item] for product in cart_list]
    cart_length = 0
    for cart in fixed_cart_list:
        cart_length_int = (int(cart[2]))
        cart_length = cart_length + cart_length_int
    coffee_menu = sqlite_functions.select_from_table('MENU')
    check_coffee = [list(row) for row in coffee_menu]
    
    return render_template('checkout.html', form = form, cart_sum = cart_sum_int, cart_length = cart_length, cart_items = cart_items, check_coffee = check_coffee)



if __name__ == '__main__':
    app.run(debug=True)


   

