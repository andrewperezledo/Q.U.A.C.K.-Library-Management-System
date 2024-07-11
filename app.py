<<<<<<< Updated upstream
from flask import Flask, render_template, request, url_for, redirect

# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)




@app.route('/', methods=('GET', 'POST'))

def homepage():

    return render_template('homepage.html')


@app.route('/create-user', methods=('GET', 'POST'))

def create_user():
    if request.method == 'POST':
        name = request.form.get('content')
        student = request.form.get('degree')
        # search if user exists
        # Process the form data (e.g., save to database)
        
        # Redirect to the homepage route
        
        return redirect(url_for('home_user', username=name))
    return render_template('create_user.html')


@app.route('/home-user', methods = ('GET', "POST"))

def home_user():
    username = request.args.get('username')
    return render_template('home_user.html', username = username)


if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.debug = 1

=======
from flask import Flask, render_template, request, url_for, redirect
from DatabaseTools.databasetools import userCreation 
# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))

def homepage():

    return render_template('homepage.html')


@app.route('/create-user', methods=('GET', 'POST'))

def create_user():
    if request.method == 'POST':
        name = request.form.get('content_username')
        password = request.form.get('content_password')
        student = request.form.get('content_student')
        

        # returns something like "matched_user" if already exists, or "failed" or "success"
        create_status = userCreation(name, password, "member")
        
        # Redirect to the homepage route
        return redirect(url_for('home_user', username=name))
    return render_template('create_user.html')


@app.route('/login', methods=('GET', 'POST'))

def login():
    if request.method == 'POST':
        name = request.form.get('content_username')
        password = request.form.get('content_password')

        # CHECK IF USER/PASSWORD EXIST AND ARE CORRECT
       
        
        # Redirect to the user homepage route
        return redirect(url_for('home_user', username=name))
    return render_template('login.html')

@app.route('/home-user', methods = ('GET', "POST"))

def home_user():
    username = request.args.get('username')
    return render_template('home_user.html', username = username)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html")

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.run(debug=True)

>>>>>>> Stashed changes
