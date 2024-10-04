from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

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

@app.route('/menu')
def menu():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('welcome-index.html')
@app.route('/rewards')
def rewards():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('welcome-index.html')
@app.route('/employ')
def employ():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('welcome-index'))

    # show the form, it wasn't submitted
    return render_template('welcome-index.html')

if __name__ == '__main__':
    app.run(debug=True)