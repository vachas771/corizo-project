from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import User, Product

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce_db'  # MongoDB URI
app.config['SECRET_KEY'] = 'your_secret_key'

mongo = PyMongo(app)
login_manager = LoginManager(app)

# Initialize user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query(user_id)

@app.route('/')
def home():
    products = Product.query()  # Get products from MongoDB
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query({'email': email, 'password': password}).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=password)
        new_user.save()  # Save to MongoDB
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
