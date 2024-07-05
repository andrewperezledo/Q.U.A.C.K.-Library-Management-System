from flask import Flask, render_template, request, url_for, redirect

# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.debug = 1

@app.route('/', methods=('GET', 'POST'))

def form_buttons_example():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        # Process the form data (e.g., save to database)
        
        # Redirect to the homepage route
        return redirect(url_for('homepage'))
    return render_template('form_and_button.html')



@app.route('/home', methods=('GET', 'POST'))

def homepage():
    return render_template('homepage.html')