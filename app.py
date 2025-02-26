from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector as sql
import random
from config import DB_CONFIG

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'securekey_22447435'

# MySQL Database Connection
db = sql.connect(**DB_CONFIG)
mycur = db.cursor()

# Ensure Users Table Exists
mycur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        accno INT UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        phno VARCHAR(10) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        address TEXT NOT NULL,
        balance INT DEFAULT 10000 CHECK (balance >= 0)
    )
""")
db.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phno = request.form['phno']
        password = request.form['password']
        address = request.form['address']
        accno = random.randint(11111, 99999)
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            mycur.execute("INSERT INTO users (accno, name, phno, password_hash, address) VALUES (%s, %s, %s, %s, %s)",
                          (accno, name, phno, password_hash, address))
            db.commit()
            flash(f'Account Created! Your Account Number is {accno}', 'success')
            return redirect(url_for('login'))
        except sql.Error:
            flash('Error: Account not created. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        accno = request.form['accno']
        password = request.form['password']

        mycur.execute("SELECT * FROM users WHERE accno = %s", (accno,))
        user = mycur.fetchone()

        if user and bcrypt.check_password_hash(user[4], password):
            session['accno'] = user[1]
            session['name'] = user[2]
            session['balance'] = user[6]
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'accno' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', name=session['name'], balance=session['balance'])

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'accno' not in session:
        return redirect(url_for('login'))

    amount = int(request.form['amount'])
    new_balance = session['balance'] + amount

    mycur.execute("UPDATE users SET balance = %s WHERE accno = %s", (new_balance, session['accno']))
    db.commit()
    session['balance'] = new_balance
    flash('Deposit Successful!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'accno' not in session:
        return redirect(url_for('login'))

    amount = int(request.form['amount'])
    if amount > session['balance']:
        flash('Insufficient Balance!', 'danger')
    else:
        new_balance = session['balance'] - amount
        mycur.execute("UPDATE users SET balance = %s WHERE accno = %s", (new_balance, session['accno']))
        db.commit()
        session['balance'] = new_balance
        flash('Withdrawal Successful!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
