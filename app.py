from flask import Flask, render_template, request, url_for, redirect, session, flash
from DatabaseTools.databasetools import *
from datetime import datetime
from DatabaseTools.databasekeys import session_secret_key

# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

# https://www.youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX
# Flask tutorial by Tech With Tim on YouTube proved to be very insightful for out project

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
            data = findPost("Userdata", "Users", "_id", username)
            return render_template('member.html', username=username, inventory=inventory,
                                   booklength=len(inventory[0]), movielength=len(inventory[1]),
                                   reservations=data["reservations"], num_res=len(data["reservations"]))
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

# In here somewhere, change it so that members get routed to "reservation_page"
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
        if parameter != "new_items":
            flash(f"You searched for {medium} with {parameter}s like '{search_text}'.", 'info')
            searched_items = generalSearch("Inventory", medium, parameter, search_text)

            if len(searched_items) == 0:
                flash("Your search did not match any items.", "info")
                #return redirect(url_for('catalog'))
        else:
            data = userSearch(session["username"])
            history = data["history"]
            items = {}
            if medium == "Movies":
                items = getAllMovies()
            else:
                items = getAllBooks()
            for item in items:
                newItem = True
                for history_item in history:
                    if item["title"] == history_item:
                        print("MATCH")
                        newItem = False
                if newItem:
                    searched_items.append(item)
            flash(f"You searched for {medium} you have not checked out before.")

        return render_template("catalog.html", len=len(searched_items), books=searched_items)

    all_books = getAllBooks()
    return render_template("catalog.html", len=len(all_books), books=all_books)


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

        return render_template('checkout.html', book=book)

    else:
        flash('You must be logged in to checkout.', 'info')
        return redirect(url_for('catalog'))


@app.route("/manageinventory", methods=('GET', 'POST'))
def manage_inventory():
    if 'username' in session:
        if session["usertype"] != "member":
            item_collection = str(request.form.get('type'))
            if item_collection == "Books":
                item_isbn = str(request.form.get('isbn'))
                print(f"ISBN: {item_isbn}, Collection: {item_collection}, Results: books")
                books = ISBNSearch(item_isbn, item_collection)
                book = books[0]
            else:
                item_isbn = int(request.form.get('isbn'))
                print(f"ISBN: {item_isbn}, Collection: {item_collection}, Results: movies")
                books = ISBNSearch(item_isbn, item_collection)
                book = books[0]

            return render_template('edit_inventory.html', book=book)
    return redirect(url_for('homepage'))


@app.route("/updatinginventory", methods=('GET', 'POST'))
def inventory_updating():
    if 'username' in session:
        if session["usertype"] != "member":
            field = request.form.get('new_field')
            value = request.form.get('new_value')
            item_collection = str(request.form.get('type'))
            if item_collection == "Books":
                item_isbn = str(request.form.get('isbn'))
                if field == "DELETE":
                    deletePost("Inventory", item_collection,"_id",item_isbn)
                    return redirect(url_for('catalog'))
                updatePost("Inventory", "Books",
                           "_id", item_isbn,
                           field, value)
            else:
                item_isbn = int(request.form.get('isbn'))
                if field == "DELETE":
                    deletePost("Inventory", item_collection,"_id",item_isbn)
                    return redirect(url_for('catalog'))
                updatePost("Inventory", "Movies",
                           "_id", item_isbn,
                           field, value)
    return redirect(url_for('catalog'))

@app.route("/create-item", methods=('GET', 'POST'))
def item_creation():
    if 'username' in session:
        if session["usertype"] != "member":
            return render_template('create_item.html')
    return redirect(url_for('/create-item'))

@app.route("/creating-item", methods=('GET', 'POST'))
def inprogress_item_creation():
    if request.form.get('type') == "Book":
        post = {'_id':request.form.get('isbn'),'title': str(request.form.get('title')),
                'author': str(request.form.get('author')), 'release_year': str(request.form.get('release_year')),
                'publisher': str(request.form.get('publisher')), 'cover_img': str(request.form.get('cover_img')),
                'availability': True, 'due_date': 'none', 'copies': '1',
                'description': str(request.form.get('description')), 'genre': str(request.form.get('genre')),
                'location': str(request.form.get('location')), 'version': '1', 'copies_available': 1,
                'reserved_by': []}
        addPost("Inventory","Books",post)
    else:
        db = cluster["Inventory"]
        coll = db["Movies"]
        index = coll.count_documents({})
        post = {'_id': int(index + 1), 'title': str(request.form.get('title')),
                'genre': str(request.form.get('genre')),
                'release_year': str(request.form.get('release_year')),
                'audience_score': "N/A", 'rotten_score': "N/A",
                'gross' : "N/A",
                'availability': True, 'reserved_by': [],
                'copies': '1', 'copies_available': 1,
                'due_date': 'none'
                }
        coll.insert_one(post)
    return redirect(url_for('homepage'))

# this function actually checks out the book as user is logged in
@app.route("/check", methods=('GET', 'POST'))
def check():
    if request.method == "POST":
        isbn = request.form['isbn']
        collection = request.form['type']
        username = request.form['username']
    user = userSearch(username)

    if user:
        if collection == "Books":
            items = ISBNSearch(isbn, collection)
            item = items[0]

            if item['reserved_by']:
                if item['reserved_by'][0] != username:
                    message = f"Item reserved by '{item['reserved_by'][0]}'"
                    flash(message, 'info')
                    return redirect(url_for('catalog'))
                else:
                    #update user reservations 
                    user = userSearch(username)
                    user_reservations = user['reservations']
                    user_new_reservations = user_reservations[1:]
                    updatePost("Userdata", "Users", "_id", username, "reservations", user_new_reservations)
                    #update item reservation
                    reserved_by = item['reserved_by']
                    new_reserved_by = reserved_by[1:]
                    updatePost("Inventory", "Books", "_id", isbn, "reserved_by", new_reserved_by)

            status = bookCheckout(isbn, username)
            if status == "User has overdue items.":
                flash(status, "info")
            elif status == "Book unavailable":
                # logic for redirecting to queue page
                flash(status, "info")
                #session["item_isbn"] = isbn
                #return redirect(url_for('reservation_page'))

            else:
                flash(status, "info")

        elif collection == "Movies":
            items = ISBNSearch(int(isbn), collection)
            item = items[0]

            if item['reserved_by']:
                if item['reserved_by'][0] != username:
                    message = f"Item reserved by '{item['reserved_by'][0]}'"
                    flash(message, 'info')
                    return redirect(url_for('catalog'))
                else:
                    #update user reservations 
                    user = userSearch(username)
                    user_reservations = user['reservations']
                    user_new_reservations = user_reservations[1:]
                    updatePost("Userdata", "Users", "_id", username, "reservations", user_new_reservations)
                    #update item reservation
                    reserved_by = item['reserved_by']
                    new_reserved_by = reserved_by[1:]
                    updatePost("Inventory", "Movies", "_id", int(isbn), "reserved_by", new_reserved_by)

            status = movieCheckout(int(isbn), username)
            if status == "User has overdue items.":
                flash(status, "info")
            elif status == "Movie unavailable":
                # logic for redirecting to queue page
                flash(status, 'info')
            else:
                flash(status, "info")
    else:
        flash("User Does Not Exist.", 'info')

    return redirect(url_for('catalog'))


@app.route("/return", methods=('GET', 'POST'))
def item_return():
    if "username" in session:
        if request.method == "POST":
            isbn = request.form['isbn']
            collection = request.form['type']
            username = request.form['username']
        try:
            if collection == "Books":
                status = bookReturn(isbn, username)
                flash(status, 'info')
            else:
                status = movieReturn(int(isbn), username)
                flash(status, 'info')
        except:
            flash('Return Failed', 'info')
        return redirect(url_for('catalog'))


@app.route("/reservation", methods=('GET', 'POST'))
def reservation_page():
    if "username" in session:
        '''isbn = session['item_isbn']
        if isbn is int:
            item = ISBNSearch(isbn, "Movies")
        else:
            item = ISBNSearch(isbn, "Books")
        item_title = item[0]["title"]'''
        if request.method == "POST":
            item_id = request.form.get('item_id')
            item_medium = request.form.get('medium')
            print(f"ID: {item_id}  Medium: {item_medium} ***************************************")
            if item_medium == "Books":
                items = ISBNSearch(item_id, str(item_medium))
            else:
                items = ISBNSearch(int(item_id), str(item_medium))

            item = items[0]

        waittime = len(item["reserved_by"]) * 3 + 3
        return render_template('reservation.html', item_id=item['_id'], item=item, waittime=str(waittime))


@app.route("/reservation/joining", methods=('GET', 'POST'))
def listjoin():
    if "username" in session:
        if request.method == 'POST':
            item_id = request.form.get('item_id')
            reserveItem(item_id, session['username'])
            flash("Reservation successful.", "info")
    else:
        flash("Reservation failed.", "info")
    return redirect(url_for('catalog'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('usertype', None)
    return redirect(url_for('homepage'))

# Changes here too
@app.route('/admin/manage-employees', methods=['GET', 'POST'])
def manage_employees():
    if 'usertype' in session and session['usertype'] == 'admin':
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add':
                username = request.form['username']
                password = request.form['password']
                usertype = request.form['usertype']
                result = admin_create_user(username, password, usertype)
                if result == "success":
                    flash('User added successfully', 'success')
                else:
                    flash('Failed to add user', 'error')

            elif action == 'update':
                username = request.form['username']
                new_role = request.form['new_role']
                if updateUserRole(username, new_role):
                    flash('User role updated successfully', 'success')
                else:
                    flash('Failed to update user role', 'error')

            elif action == 'delete':
                username = request.form['username']
                if admin_delete_user(username):
                    flash('User deleted successfully', 'success')
                else:
                    flash('Failed to delete user', 'error')

            return redirect(url_for('manage_employees'))

        users = getAllUsers()
        return render_template('manage_employees.html', users=users)
    else:
        return redirect(url_for('homepage'))

# More new griffin code
@app.route('/employee/manage-members', methods=['GET', 'POST'])
def manage_members():
    if 'usertype' in session and session['usertype'] in ['employee', 'admin']:
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add':
                username = request.form['username']
                password = request.form['password']
                result = admin_create_user(username, password, 'member')
                if result == "success":
                    flash('Member added successfully', 'success')
                else:
                    flash('Failed to add member', 'error')

            elif action == 'delete':
                username = request.form['username']
                if admin_delete_user(username):
                    flash('Member deleted successfully', 'success')
                else:
                    flash('Failed to delete member', 'error')

            return redirect(url_for('manage_members'))

        members = [user for user in getAllUsers() if user['usertype'] == 'member']
        return render_template('manage_members.html', members=members)
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
    return redirect(url_for("eventspecific", year=year, month=month, day=day, period=period))


@app.route("/events/e=", methods=['GET'])
def eventspecific(year=None, month=None, day=None, period=None):
    selectedYear = request.args.get("year", type=int)
    selectedMonth = request.args.get("month", type=int)
    selectedDay = request.args.get("day", type=int)
    selectedPeriod = request.args.get("period", type=int)

    try:
        selectedEventDate = {"year": selectedYear, "month": selectedMonth, "day": selectedDay, "period": selectedPeriod}
        currDate = datetime(selectedYear, selectedMonth, selectedDay)
        if selectedPeriod < 1 or selectedPeriod > 7:
            raise Exception("Period out of bounds")
    except:
        return render_template("not_found.html")

    # Easy passing of dates for create event
    session["year"] = selectedYear
    session["month"] = selectedMonth
    session["day"] = selectedDay
    session["period"] = selectedPeriod

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

    return render_template("events.html", event=selectedEventDate, slotAvailable=isSlotAvailable(selectedEventDate),
                           month=currDate.strftime("%B"), usertype=usertype)


@app.route('/get-event-by-day', methods=['POST'])
def get_events_by_day():
    events = []
    if request.method == "POST":
        data = request.get_json()
        events = getEventsByDate(f"{data['year']}-{data['month']}-{data['day']}")

    return events


@app.route('/event-rsvp/', methods=['GET'])
def event_rsvp(year=None, month=None, day=None, period=None):
    selectedYear = request.args.get("year", type=int)
    selectedMonth = request.args.get("month", type=int)
    selectedDay = request.args.get("day", type=int)
    selectedPeriod = request.args.get("period", type=int)
    selectedEventDate = {"year": selectedYear, "month": selectedMonth, "day": selectedDay, "period": selectedPeriod}
    if 'usertype' in session:
        if not incrimentRSVP(selectedEventDate):
            flash("An error has occured", "error")
        else:
            flash("RSVP addded", "info")
    else:
        flash("Must be logged in to RSVP events", "error")
    return redirect(
        url_for("eventspecific", year=selectedYear, month=selectedMonth, day=selectedDay, period=selectedPeriod))


@app.route('/events/create/', methods=['GET','POST'])
def event_create():
    if request.method == 'POST':
        date = request.form.get("date")
        period = request.form.get("period")
        title = request.form.get("title")
        desc = request.form.get("desc")
        contact = request.form.get("contact")
        splash = request.form.get("splash")
        user = request.form.get("user")
        approved = True if request.form.get("approved") else False

        status = eventCreation(date, period, title, desc, contact, splash, user, 0, approved)
        if status == "Time Slot Taken":
            flash("Time slot already pending approval", "error")
        elif status == "fail":
            flash("Something when wrong, try again later", "error")
        else:
            flash("Event successfully added")

    selectedYear=''
    selectedMonth=''
    selectedDay=''
    selectedPeriod=''
    selectedDate = datetime.now().strftime("%Y-%m-%d")
    currDate = datetime.now().strftime("%Y-%m-%d")

    if "year" in session:
        selectedYear = session["year"]
        selectedMonth = session["month"]
        selectedDay = session["day"]
        selectedPeriod = session["period"]
        selectedDate = f"{selectedYear}-{int(selectedMonth):02d}-{int(selectedDay):02d}"
    if 'usertype' in session:
        if session['usertype'] == "admin" or session['usertype'] == "employee":
            return render_template("create_event.html", selectedDate=selectedDate, selectedPeriod=selectedPeriod,
                currDate=currDate, usertype=session["usertype"])
    flash("Must be library staff member to create events", "error")
    return redirect(url_for('login'))


@app.route('/events/manage/', methods=['GET', 'POST'])
def event_manage():
    if 'usertype' not in session or session['usertype'] == "member":
        flash("Must be library staff member to manage events", "error")
        return redirect(url_for('login'))

    events = []
    events.extend(findManyPost("Events", "Events", "approved", False))
    events.extend(findManyPost("Events", "Events", "approved", True))

    return render_template("manage_events.html", events=events, num_events = len(events))



time_slots = ["9:00am - 10:00am", "10:30am - 11:30am", "12:00pm - 1:00pm", "1:30pm - 2:30pm", "3:00pm - 4:00pm", "4:30pm - 5:30pm", "6:00pm - 7:00pm"]
@app.route('/events/manage/edit/', methods=['GET', 'POST'])
def event_edit():
    if request.method == 'POST':
        if request.form.get("edit"):
            # For the purpose of passing in date of event selected
            date = request.form.get("edit").split('-')

            session["year"] = int(date[0])
            session["month"] = int(date[1])
            session["day"] = int(date[2])
            session["period"] = int(date[3])
            session["event"] = f"{session["year"]}-{session["month"]}-{session["day"]}-{session["period"]}"

            selectedDate = f"{session["year"]}-{session["month"]:02d}-{session["day"]:02d}"
            currDate = datetime.now().strftime("%Y-%m-%d")


            return render_template("edit_events.html", event=findPost("Events", "Events", "_id", f"{request.form.get("edit")}"),
                                   selectedDate=selectedDate, selectedPeriod=session["period"], currDate=currDate)
        else:
            if request.form.get("date"):
                date = request.form.get("date")
                date = date.split('-')

                if findPost("Events", "Events", "_id", f"{int(date[0])}-{int(date[1])}-{int(date[2])}-{request.form.get("period")}"):
                    flash("Time slot already occupied", "error")
                    redirect(url_for("event_manage"))
                else:
                    new_id = f"{int(date[0])}-{int(date[1])}-{int(date[2])}-{request.form.get("period")}"
                    changePostid("Events", "Events", session["event"], new_id)
                    updatePost("Events", "Events", "_id", new_id, "time",
                            time_slots[request.form.get("period", type=int) - 1])
            else:
                # To sustain boolean approved status
                new_val = request.form.get("value")
                if new_val == "true":
                    new_val = True
                elif new_val == "false":
                    new_val == False

                updatePost("Events", "Events", "_id", session["event"], f"{request.form.get("key")}", new_val)

    flash("Event successfully updated")
    return redirect(url_for("event_manage"))


@app.route('/events/manage/delete/', methods=['GET', 'POST'])
def event_delete():
    if request.method == 'POST':
        deletePost("Events", "Events", "_id", f"{request.form.get("delete")}")
    return redirect(url_for("event_manage"))


@app.errorhandler(404)
@app.errorhandler(405)
def not_found(e):
    return render_template("not_found.html")


if __name__ == '__main__':  # DEVELOPMENT DEBUG MODE
    app.run(debug=True)
