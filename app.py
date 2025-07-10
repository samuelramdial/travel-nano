from flask import Flask, render_template, redirect, url_for, request, session, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import requests, json
from dotenv import load_dotenv
import os
from datetime import date
from decimal import Decimal
# import pytz

load_dotenv()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'ITSC-3155-Team-7'

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

conn = psycopg2.connect(user=db_user, password=db_pass, host=db_host, port=db_port, dbname=db_name)

@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM web_user WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO web_user (fullname, username, user_password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using database
        cursor.execute('SELECT * FROM web_user WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['user_password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['web_user_id'] = account['web_user_id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM web_user WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
if __name__ == "__main__":
    app.run(debug=True)
 
@app.route('/currency', methods = ['GET', 'POST'])
def currency():
    url = "https://v6.exchangerate-api.com/v6/45d38949eb39005b6b5c0c15/latest/USD"
    if request.method == 'POST':
        response = requests.get(url) 
        data = response.json()
        countries = data['conversion_rates']
        class currencyConversion: 
            def __init__(self, url):
                self.data = data 
                self.currencies = self.data['conversion_rates']

            def convert(self, currencyFrom, currencyTo, amount):
                if currencyFrom != 'USD':
                    amount = float(amount) / self.currencies[currencyFrom]
                amount = round(float(amount) * self.currencies[currencyTo],2)
                return amount
        fromCurrency = request.form['fromCurrency']
        toCurrency = request.form['toCurrency']
        amount = request.form['amount']
        conversion = currencyConversion(url)
        finalConversion = conversion.convert(fromCurrency, toCurrency, amount)
        return render_template('currency.html', fromCurrency = fromCurrency, toCurrency = toCurrency, amount = amount, finalConversion = finalConversion)
    
    return render_template('currency.html', fromCurrency = 'USD', toCurrency = 'CAD', amount = 1, finalConversion = 1.34)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create_post', methods = ['POST', 'GET'])
def create_post():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method != 'POST':
        return render_template('post_submission_page.html')
    
    # check if the post request has the file part
    if 'upload-file' not in request.files:
        flash('No file part')
        return redirect('post_submission_page.html')
    uploadFile = request.files['upload-file']
    # If the user does not select a file, the browser submits and
    # empty file with a filename
    if uploadFile.filename == '':
        flash('No selected file')
        return redirect('post_submission_page.html')
    if uploadFile and allowed_file(uploadFile.filename):
        filename = secure_filename(uploadFile.filename)
        uploadFile.save(os.path.join('static', 'post_images', filename))

    uploadTitle = request.form['title-post']
    uploadCaption = request.form['caption']
    username = session['username']
    temp_date = date.today()
    data_month = temp_date.strftime('%B')
    data_day = temp_date.strftime('%d')
    data_year = temp_date.strftime('%Y')
    

    cursor.execute('INSERT INTO post (post_title, picture_file, caption, username, post_month, post_day, post_year)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (uploadTitle, filename, uploadCaption, username, data_month, data_day, data_year))
    
    conn.commit()

    return render_template('post_submission_page.html')

 # posts list page
@app.route('/posts',methods=['GET'])
def postList():
    if 'loggedin' in session:

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM post')
        postsList = cursor.fetchall()
        return render_template('posts.html', posts = postsList)
    return redirect(url_for('login'))
   
#Each post page
@app.route('/post/<string:post_title>',methods=['GET','POST'])
def postItem(post_title):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'loggedin' in session:
        if 'post_id' in request.args:
            post_id = int(request.args.get('post_id'))
            cursor.execute('SELECT * FROM post WHERE post_id =%s', [post_id])
            postItem  = cursor.fetchone() #posts[post_id]
        #     comment = ''
        #     if request.method == 'POST':
        # # Get the comment text from the form data
        #         comment = request.form['comment']
        # there is to create/fetch comment from db
                
            return render_template('postItem.html', postItem = postItem)
        return flash('No post')
    return redirect(url_for('login'))
    # return render_template("<h1 class='container'> NOT FOUND !!</h1>")   
