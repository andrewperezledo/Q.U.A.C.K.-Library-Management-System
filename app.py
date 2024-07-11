from flask import Flask, render_template, request, url_for, redirect,session
from DatabaseTools.databasetools import userCreation 
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
        name = request.form.get('content')
        student = request.form.get('degree')
        # SEARCH IF USER ALREADY EXISTS!!!!!

        # Process the form data (e.g., save to database)
        # userCreation(name, "password123", "member")
        session['username'] = name
        
        # Redirect to the homepage route
        return redirect(url_for('home_user', username=name))
    return render_template('create_user.html')


@app.route('/home-user', methods = ('GET', "POST"))

def home_user():
    if "username" in session:
        username = request.args.get('username')
        return render_template('home_user.html', username = username)
    else:
        return redirect(url_for('create_user'))

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('create_user'))

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.run(debug=True)

