from flask import Flask, url_for, request, jsonify, render_template, session, redirect
from flask_mysqldb import MySQL
from decouple import config
app = Flask(__name__)

app.secret_key = config('SECRET',default=1234567)

# MySQL Configuration
app.config['MYSQL_HOST']=config('DB_HOST')
app.config['MYSQL_USER']=config('DB_USER')
app.config['MYSQL_PASSWORD']=config('DB_PASSWD')
app.config['MYSQL_DB']=config('DB_NAME')

mysql = MySQL(app)

# Sports and time slots
sports = ['Football', 'Cricket', 'Tennis', 'Basketball']
time_slots = ['09:00-10:00', '13:00-15:00', '16:00-17:00', '18:00-19:00']

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template('index.html', logged_in=logged_in)

@app.route('/register', methods=['POST'])
def register():
    user = request.json.get('user')
    passwd = request.json.get('passwd')
    cursor = mysql.connection.cursor()
    
    # Check for existing username
    cursor.execute('SELECT * FROM users WHERE user = %s', (user,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        cursor.close()
        return jsonify({'message': 'Username already exists, try again.'}), 400

    # Insert new user
    cursor.execute('INSERT INTO users (user, passwd) VALUES (%s, %s)', (user, passwd))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User added successfully.'}), 201

@app.route('/login', methods=['POST'])
def login():
    user = request.json.get('user')
    passwd = request.json.get('passwd')
    cursor = mysql.connection.cursor()
    
    # Fetch user from database
    cursor.execute('SELECT * FROM users WHERE user = %s', (user,))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.close()
        return jsonify({'message': 'User not found.'}), 404

    # Validate password
    if existing_user[2] != passwd:
        cursor.close()
        return jsonify({'message': 'Invalid password.'}), 401

    session['username'] = existing_user[1]  # Store username in session
    cursor.close()
    return jsonify({'message': 'Login successful.'}), 200

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')  # Redirect to index if not logged in
    
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        sport = request.json.get('sport')
        time_slot = request.json.get('time_slot')
        date = request.json.get('date')
        
        # Check if the slot is already booked by anyone else for the same date
        cursor.execute('SELECT * FROM reservations WHERE sport = %s AND time_slot = %s AND date = %s', (sport, time_slot, date))
        existing_reservation = cursor.fetchone()
        
        if existing_reservation:
            cursor.close()
            return jsonify({'message': 'This time slot is already booked.'}), 400
        
        # Reserve the slot for the logged-in user
        cursor.execute('INSERT INTO reservations (user, sport, time_slot, date) VALUES (%s, %s, %s, %s)', (session['username'], sport, time_slot, date))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Reservation made successfully.'}), 201

    # Fetch user's reservations
    cursor.execute('SELECT * FROM reservations WHERE user = %s', (session['username'],))
    user_reservations = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html', username=session['username'], sports=sports, time_slots=time_slots, user_reservations=user_reservations)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove username from session
    return jsonify({'message': 'Successfully logged out.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
