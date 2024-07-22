from flask import Flask, render_template, request, url_for, redirect, session, flash
from DatabaseTools.databasetools import *
from datetime import datetime
from DatabaseTools.databasekeys import session_secret_key

# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)
app.secret_key = session_secret_key


@app.route('/', methods=('GET', 'POST'))
def homepage():
    username = request.args.get('username')
    if 'username' in session:
        usertype = session['usertype']
        username = session['username']
        if usertype == 'admin':
            return render_template('admin.html', username=username)
        elif usertype == 'employee':
            return render_template('employee.html', username=username)
        else:  # member
            return render_template('member.html', username=username)
    else:
        return render_template('homepage.html')
    # return render_template('homepage.html')




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
            return redirect(url_for('create_user'))
        # Redirect to the homepage route
        else:
            flash("Creation Failed", "info")
            return redirect(url_for(homepage))
        return redirect(url_for('homepage', username=name))
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
            return redirect(url_for('homepage'))
        else:
            flash("Invalid username or password", "info")
            return redirect(url_for('login'))

    return render_template('login.html')


# @app.route('/home-user', methods=('GET', "POST"))
# def home_user():
#     username = request.args.get('username')
#     if 'username' in session:
#         usertype = session['usertype']
#         username = session['username']
#         if usertype == 'admin':
#             return render_template('admin.html', username=username)
#         elif usertype == 'employee':
#             return render_template('employee.html', username=username)
#         else:  # member
#             return render_template('member.html', username=username)
#     else:
#         return render_template('homepage.html')
    

# IN CONSTRUCTION, CATALOG CHECKOUT BUTTON TO CHECKOUT PAGE FOR SPECIFIC BOOK
@app.route("/catalog", methods=('GET', 'POST'))
def catalog():
    all_books = getAllBooks()
    return render_template("catalog.html", len = len(all_books), books = all_books)


@app.route("/checkout", methods=('GET', 'POST'))
def checkout():
    if 'username' in session:
        # This is all in POST method
        book_isbn = str(request.form.get('isbn'))
        books = ISBNSearch(book_isbn)
        book = books[0]
        return render_template('checkout.html', book = book)
    else:
         flash('You must be logged in to checkout.', 'info')
         return redirect(url_for('catalog'))

# this function actually checks out the book as user is logged in
@app.route("/check", methods=('GET', 'POST'))
def check():
    if request.method == "POST":
        isbn = request.form['isbn']

    username = session['username']

    status = bookCheckout(isbn, username)

    if status == "Book unavailable":
        flash("Book is unavailable.", "info")

    elif status == "Book does not exist":
        flash("Book does not exist.", "info")

    else:
        flash("Item successfully checked out.", "info")

    return redirect(url_for('catalog'))
       
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('usertype', None)
    return redirect(url_for('homepage'))

@app.route('/admin/manage-employees')
def manage_employees():
    if 'usertype' in session and session['usertype'] == 'admin':
        users = getAllUsers()  # You'll need to create this function in databasetools.py
        return render_template('manage_employees.html', users=users)
    else:
        return redirect(url_for('homepage'))

@app.route('/admin/update-user-role', methods=['POST'])
def update_user_role():
    if 'usertype' in session and session['usertype'] == 'admin':
        username = request.form.get('username')
        new_role = request.form.get('new_role')
        updateUserRole(username, new_role)
        return redirect(url_for('manage_employees'))
    else:
        return redirect(url_for('homepage'))

@app.route("/events", methods=['GET', 'POST'])
def events():
    # eventCreation(datetime.today().strftime('%Y-%m-%d') + "-01", "Birthday day!", "My birthday today! Call this number to RSVP!", "123-456-7890")
    events = getEventsByDate(datetime.today().strftime('%Y-%m-%d'))
    return render_template("events.html", events=events)

# Add "/events/register" route. Blueprint? Probably not worth it
# if not logged in, redirect to login, then back to register page

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.run(debug=True)
