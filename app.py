from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace this with a stronger secret key in production

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulated user database (replace with real database later)
users = {
    "admin": {"password": "password"}  # username: admin, password: password
}

# Flask-Login User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    try:
        with open('ships.json', 'r') as f:
            ships = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ships = []
    return render_template('index.html', ships=ships, username=current_user.id)

@app.route('/add_ship', methods=['POST'])
@login_required
def add_ship():
    name = request.form['name']
    last_maintenance = request.form['last_maintenance']
    ship_type = request.form['ship_type']
    capacity = request.form['capacity']
    try:
        with open('ships.json', 'r') as f:
            ships = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ships = []

    ships.append({
        'name': name,
        'last_maintenance': last_maintenance,
        'ship_type': ship_type,
        'capacity': capacity
    })

    with open('ships.json', 'w') as f:
        json.dump(ships, f, indent=4)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
