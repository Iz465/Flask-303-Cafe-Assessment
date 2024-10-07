from flask import Flask, redirect, url_for, request, render_template
import sqlite3
import menuhandler
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

database_dict = getdb_dict()

@app.route('/')
def index():
    return render_template('welcome-index.html')
#http://127.0.0.1:5000/admin
@app.route('/admin')
def hello_admin():
    return "hello Admin"

#http://127.0.0.1:5000/guest/<guest>
@app.route('/home')
def home():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('welcome-index.html')

@app.route('/menu', methods=["POST","GET"])
def menu():
    data_dict = database_dict
    handler = menuhandler.MenuHandler(data_dict)
    if request.method == 'POST':
        sortbyvalue = request.form.get("sortdropdown")
        print("SORTING BY VALUE: ",str(sortbyvalue))

        return render_template('menu-index.html', sortbyvalue = sortbyvalue, data=handler.sorteddata(sortbyvalue))

    # show the form, it wasn't submitted
    return render_template('menu-index.html', data = data_dict)

@app.route('/rewards')
def rewards():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('rewards-index.html')
@app.route('/employ')
def employ():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('employ-index.html')


if __name__ == '__main__':
    app.run(debug=True)