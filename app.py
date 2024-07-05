from flask import Flask, render_template

# to run, export this file with export FLASK_APP=home, export FLASK_DEBUG=1
# to run mutiple apps, use -p like this: flask run -p 5001 *******to change port 
# templates for the html & js inside html, static for CSS, JavaScript, & images

app = Flask(__name__)

if __name__ == '__main__': # DEVELOPMENT DEBUG MODE
    app.debug = 1

@app.route('/')

def form_buttons_example():
    return render_template('form_and_button.html')
