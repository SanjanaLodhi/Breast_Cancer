from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import numpy as np
import pickle

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'breast cancer'  # Corrected typo
mysql = MySQL(app)

# Load the trained model (ensure you have the correct path to your model)
model = pickle.load(open("savedmodel.sav", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html')

@app.route('/result', methods=['POST'])  # This route will handle the prediction
def result():
    if request.method == 'POST':
        # Collect the form data
        mean_radius = float(request.form['mean_radius'])
        mean_texture = float(request.form['mean_texture'])
        mean_perimeter = float(request.form['mean_perimeter'])
        mean_area = float(request.form['mean_area'])
        mean_smoothness = float(request.form['mean_smoothness'])

        # Combine inputs into an array
        inputs = np.array([[mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness]])

        # Use the loaded model to make predictions
        prediction = model.predict(inputs)

        # Interpret the result (assuming 1 = benign, 0 = malignant)
        if prediction[0] == 1:
            result_text = "The Breast Cancer is Benign"
        else:
            result_text = "The Breast Cancer is Malignant"

        # Render the result on a new page
        return render_template('result.html', prediction=result_text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['name'] = users['name']
            session['email'] = users['email']
            mesage = 'Logged in successfully!'
            return render_template('predict.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email / password'
    return render_template('login.html', mesage=mesage)

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        usersName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # Corrected email regex
            mesage = 'Invalid email address!'
        elif not usersName or not password or not email:
            mesage = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (usersName, email, password))

  # Corrected query syntax
            mysql.connection.commit()
            mesage = 'You have successfully registered!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('register.html', mesage=mesage)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register1')
def regis():
    return render_template('register1.html')

if __name__ == "__main__":
    app.secret_key = 'sanjana'  # Add secret key for session management
    app.run(debug=True)