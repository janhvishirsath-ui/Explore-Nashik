from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import secrets
import os

app = Flask(__name__, template_folder='./')

# Set the secret key for session management
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",            
    password="Janhvi@2004", 
    database="userdb"        
)
cursor = db.cursor()

# Home redirects to Register page
@app.route('/')
def home():
    return redirect('/register')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        cursor.execute(sql, values)
        db.commit()

        # Show popup and redirect
        return '''
            <script>
                alert('Registration Successful!');
                window.location.href = "/login";
            </script>
        '''
    return render_template('register.html')  # Render the register.html file

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        if result:
            # Store username in session
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to 'index' route after successful login
        else:
            return redirect(url_for('login'))  # Redirect back to login if credentials are incorrect
    return render_template('login.html')  # Render the login.html file

# Index page route (This renders the index.html file)
@app.route('/index')
def index():
    try:
        return render_template('success.html')  # Render the index.html file
    except Exception as e:
        return f"Error: {str(e)}"  # Error handling if the file doesn't exist

if __name__== "__main__":
    app.run(debug=True)