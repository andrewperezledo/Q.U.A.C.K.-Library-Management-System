from flask import Flask, render_template, request, url_for, redirect, session, flash
from DatabaseTools.databasetools import *
# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)
app.secret_key = "Ducks"

@app.route('/', methods=('GET', 'POST'))

def homepage():

    return render_template('homepage.html')


@app.route('/create-user', methods=('GET', 'POST'))

def create_user():
    if request.method == 'POST':
        name = request.form.get('content_username')
        password = request.form.get('content_password')
        # returns something like "matched_user" if already exists, or "failed" or "success"
        create_status = userCreation(name, password, "member")
        
        if create_status == "success":
            session['username'] = name
            session['usertype'] = "member"
        elif create_status == "Matching Username":
            flash("Username already exists", "info")
            redirect(url_for(create_user))
        # Redirect to the homepage route
        else:
            flash("Creation Failed", "info")
            redirect(url_for(homepage))
        return redirect(url_for('home_user', username=name))
    return render_template('create_user.html')


@app.route('/login', methods=('GET', 'POST'))

def login():
    if request.method == 'POST':
        name = request.form.get('content_username')
        password = request.form.get('content_password')

        # CHECK IF USER/PASSWORD EXIST AND ARE CORRECT
        result = loginFunction(name, password)
        if result == "Login Successful.":
            userdata = userSearch(name)
            session['username'] = name
            session['usertype'] = userdata["usertype"]  # Admin, employee, or member
            return redirect(url_for('home_user', username=name))
        else:
            flash("Invalid username or password", "info")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/home-user', methods = ('GET', "POST"))

def home_user():
    username = request.args.get('username')
    if "username" in session:
        username = request.args.get('username')
        if session["usertype"] == "member":
            return render_template('member.html', username = username)
        elif session["usertype"] == "employee":
            return render_template('employee.html', username = username)
        elif session["usertype"] == "admin":
            return render_template('admin.html', username = username)
        #return render_template('home_user.html', username = username)
    else:
        return redirect(url_for('homepage'))
    
    return render_template('home_user.html', username = username)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.run(debug=True)
