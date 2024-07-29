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
            inventory = getUserInventory(username)
            return render_template('member.html', username=username,inventory=inventory,booklength=len(inventory[0]),movielength=len(inventory[1]))
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
        elif create_status == "Please enter valid username or password.":
            flash("Please enter valid username or password.", "info")
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
    if request.method == "POST":
        searched_items = []
        medium = request.form["medium"]
        parameter = request.form["parameter"]
        search_text = request.form["search-text"]

        if medium == "Movies" and parameter not in ["title", "release_year", "genre"]:
            flash("You can only search movies by Title or Year.", "info")
            return redirect(url_for('catalog'))
        
        flash(f"You searched for {medium} with {parameter}s like '{search_text}'.", 'info')
        searched_items = generalSearch(parameter, search_text, medium)

        if len(searched_items) == 0:
            flash("Your search did not match any items.", "info")
            #return redirect(url_for('catalog'))
        
        return render_template("catalog.html", len = len(searched_items), books = searched_items)
    
    all_books = getAllBooks()
    return render_template("catalog.html", len = len(all_books), books = all_books)


@app.route("/checkout", methods=('GET', 'POST'))
def checkout():
    if 'username' in session:
        # This is all in POST method
        # books have string ISBNs movies have INTEGER IDs
        item_collection = str(request.form.get('type'))
        if item_collection == "Books":
            item_isbn = str(request.form.get('isbn'))
            print(f"ISBN: {item_isbn}, Collection: {item_collection}, Results: books")
            books = ISBNSearch(item_isbn, item_collection)
            book = books[0]
        else: 
            item_isbn = int(request.form.get('isbn'))
            print(f"ISBN: {item_isbn}, Collection: {item_collection}, Results: books")
            books = ISBNSearch(item_isbn, item_collection)
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
        collection = request.form['type']
        print(f"isbn: {isbn}, collection: {collection} **************")

    username = session['username']
    if collection == "Books":
        status = bookCheckout(isbn, username)
        flash(status, "info")
        
    elif collection == "Movies":
        status = movieCheckout(int(isbn), username)
        flash(status, "info")

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


@app.route("/events/", methods=['GET'])
def events(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, period=1):
    # eventCreation("2024-7-15" + "-2", "Birthday day 2!", "Very long description. Did you know that in the year 2024 AD, the was a piece that was hidden away. This piece, coincidentally, was singular. There was a pirate that tried to find this piece with the great passion. Yes. This is the story of the one piece.", "123-456-7890")
    return redirect(url_for("eventspecific", year=year, month=month, day=day, period=period))


# year=<year>&month=<month>&day=<day>&period=<period>
@app.route("/events/e=", methods=['GET'])
def eventspecific(year=None, month=None, day=None, period=None):
    selectedYear = request.args.get("year", type=int)
    selectedMonth = request.args.get("month",  type=int)
    selectedDay = request.args.get("day",  type=int)
    selectedPeriod = request.args.get("period",  type=int)

    # If period out of bounds (not 1-7), then redirect?
    # How????
    # if (selectedPeriod is not None):
    #     if (selectedPeriod < 1):
    #         redirect(url_for("eventspecific", year=year, month=month, day=day, period=1))
    #     elif (selectedPeriod > 7):
    #         redirect(url_for("eventspecific", year=year, month=month, day=day, period=8))

    selectedEventDate = {"year": selectedYear, "month": selectedMonth, "day": selectedDay, "period": selectedPeriod}
    currDate = datetime(selectedYear, selectedMonth, selectedDay)

    usertype = ""
    if 'usertype' in session:
            if session['usertype'] == 'admin':
                usertype = "admin"
            elif session['usertype'] == 'employee':
                usertype = "employee"
            else:
                usertype = "member"
    else:
        usertype = "unauthenticated"

    return render_template("events.html", event=selectedEventDate, slotAvailable=isSlotAvailable(selectedEventDate), month=currDate.strftime("%B"), usertype=usertype)


@app.route('/get-event-by-day', methods=['POST'])
def get_events_by_day():
    events = []
    if request.method == "POST":
        data = request.get_json()
        events = getEventsByDate(f"{data['year']}-{data['month']}-{data['day']}")
    
    return events

# Returns the type of user in dict format
# @app.route('/get-user-info', methods=["POST"])
# def get_user_info():
#     user_info = {}
#     if request.method == "POST":
#         if 'usertype' in session:
#             if session['usertype'] == 'admin':
#                 user_info = {"user_type": "admin"}
#             elif session['usertype'] == 'employee':
#                 user_info = {"user_type": "employee"}
#             else:
#                 user_info = {"user_type": "member"}
#         else:
#             user_info = {"user_type": "unauthenticated"}
#     return user_info

@app.route('/event-rsvp/', methods=['GET'])
def event_rsvp(year=None, month=None, day=None, period=None):
    selectedYear = request.args.get("year", type=int)
    selectedMonth = request.args.get("month",  type=int)
    selectedDay = request.args.get("day",  type=int)
    selectedPeriod = request.args.get("period",  type=int)
    selectedEventDate = {"year": selectedYear, "month": selectedMonth, "day": selectedDay, "period": selectedPeriod}
    if 'usertype' in session:
        if not incrimentRSVP(selectedEventDate):
            flash("An error has occured", "error")
        else:
            flash("RSVP addded", "info")
    else:
        flash("Must be logged in to RSVP events", "error")
    return redirect(url_for("eventspecific", year=selectedYear, month=selectedMonth, day=selectedDay, period=selectedPeriod))


@app.route('/events/create/')
def event_create():
    if 'usertype' in session:
        if session['usertype'] == "admin" or session['usertype'] == "employee":
            return render_template("create_event.html")
    flash("Must be library staff member to create events", "error")
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.run(debug=True)
