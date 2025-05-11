from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Use a stronger secret key in production

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                addr TEXT,
                city TEXT,
                pin TEXT,
                bg TEXT,
                email TEXT UNIQUE,
                pass TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS blood (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                donorname TEXT,
                donorsex TEXT,
                qty TEXT,
                dweight TEXT,
                donoremail TEXT,
                phone TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS request (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                toemail TEXT,
                formemail TEXT,
                toname TEXT,
                toaddr TEXT
            )
        ''')
        conn.commit()

# Initialize database when the app starts
with app.app_context():
    init_db()

@app.route('/')
def home():
    user = {'username': session.get('username', '')}
    return redirect(url_for('index', user=user))

@app.route('/reg')
def add():
    return render_template('register.html')

@app.route('/addrec', methods=['POST'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            email = request.form['email']
            passs = request.form['pass']

            # Hash the password
            hashed_password = generate_password_hash(passs, method='pbkdf2:sha256')

            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO users (name, addr, city, pin, bg, email, pass) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nm, addr, city, pin, bg, email, hashed_password)
                )
                conn.commit()
            flash("Record successfully added", "success")
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash("Email already exists", "error")
            return redirect(url_for('add'))
        except Exception as e:
            flash(f"Error in insert operation: {str(e)}", "error")
            return redirect(url_for('add'))
    return redirect(url_for('add'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': session.get('username', '')}
    rows = []
    search = []

    with get_db_connection() as conn:
        if request.method == 'POST':
            val = request.form.get('search', '')
            search_type = request.form.get('type', '')

            if search_type == 'blood':
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE bg = ?", (val,))
                search = cur.fetchall()
            elif search_type == 'donorname':
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE name = ?", (val,))
                search = cur.fetchall()

        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

    return render_template('index.html', title='Home', user=user, rows=rows, search=search)

@app.route('/list')
def list():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
    return render_template("list.html", rows=rows)

@app.route('/drop')
def drop():
    try:
        with get_db_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS request")
            conn.commit()
        flash("Table dropped successfully", "success")
    except Exception as e:
        flash(f"Error dropping table: {str(e)}", "error")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        # Admin login
        if email == 'admin@bloodbank.com' and password == 'admin':
            session['username'] = email
            session['admin'] = True
            session['logged_in'] = True
            flash("Admin login successful", "success")
            return redirect(url_for('index'))

        # User login
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cur.fetchone()

                if user and check_password_hash(user['pass'], password):
                    session['username'] = user['email']
                    session['logged_in'] = True
                    flash("Login successful", "success")
                    return redirect(url_for('index'))
                else:
                    flash("Invalid email or password", "error")
                    return render_template('login.html')
        except Exception as e:
            flash(f"Login error: {str(e)}", "error")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('admin', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    totalblood = 0
    bloodtypestotal = {
        'apos': 0, 'aneg': 0, 'opos': 0, 'oneg': 0,
        'bpos': 0, 'bneg': 0, 'abpos': 0, 'abneg': 0
    }

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM blood")
        rows = cur.fetchall()

        for row in rows:
            totalblood += int(row['qty'])
            blood_type = row['type']
            if blood_type == 'A+':
                bloodtypestotal['apos'] += int(row['qty'])
            elif blood_type == 'A-':
                bloodtypestotal['aneg'] += int(row['qty'])
            elif blood_type == 'O+':
                bloodtypestotal['opos'] += int(row['qty'])
            elif blood_type == 'O-':
                bloodtypestotal['oneg'] += int(row['qty'])
            elif blood_type == 'B+':
                bloodtypestotal['bpos'] += int(row['qty'])
            elif blood_type == 'B-':
                bloodtypestotal['bneg'] += int(row['qty'])
            elif blood_type == 'AB+':
                bloodtypestotal['abpos'] += int(row['qty'])
            elif blood_type == 'AB-':
                bloodtypestotal['abneg'] += int(row['qty'])

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

    return render_template("requestdonors.html", rows=rows, totalblood=totalblood, users=users, bloodtypestotal=bloodtypestotal)

@app.route('/bloodbank')
def bloodbank():
    return render_template('adddonor.html')

@app.route('/addb', methods=['POST'])
def addb():
    if request.method == 'POST':
        try:
            blood_type = request.form['blood_group']
            donorname = request.form['donorname']
            donorsex = request.form['gender']
            qty = request.form['qty']
            dweight = request.form['dweight']
            email = request.form['email']
            phone = request.form['phone']

            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO blood (type, donorname, donorsex, qty, dweight, donoremail, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (blood_type, donorname, donorsex, qty, dweight, email, phone)
                )
                conn.commit()
            flash("Blood entry added successfully", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error adding blood entry: {str(e)}", "error")
            return redirect(url_for('bloodbank'))
    return redirect(url_for('bloodbank'))

@app.route("/editdonor/<id>", methods=['GET', 'POST'])
def editdonor(id):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM blood WHERE id = ?", (id,))
                rows = cur.fetchall()
                if not rows:
                    flash("Donor not found", "error")
                    return redirect(url_for('dashboard'))
                return render_template("editdonor.html", rows=rows)
        except Exception as e:
            flash(f"Error fetching donor: {str(e)}", "error")
            return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            blood_type = request.form['blood_group']
            donorname = request.form['donorname']
            donorsex = request.form['gender']
            qty = request.form['qty']
            dweight = request.form['dweight']
            email = request.form['email']
            phone = request.form['phone']

            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE blood SET type = ?, donorname = ?, donorsex = ?, qty = ?, dweight = ?, donoremail = ?, phone = ? WHERE id = ?",
                    (blood_type, donorname, donorsex, qty, dweight, email, phone, id)
                )
                conn.commit()
            flash("Donor updated successfully", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error updating donor: {str(e)}", "error")
            return redirect(url_for('dashboard'))

@app.route("/myprofile/<email>", methods=['GET', 'POST'])
def myprofile(email):
    if request.method == 'GET':
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE email = ?", (email,))
                rows = cur.fetchall()
                if not rows:
                    flash("User not found", "error")
                    return redirect(url_for('index'))
                return render_template("myprofile.html", rows=rows)
        except Exception as e:
            flash(f"Error fetching profile: {str(e)}", "error")
            return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['addr']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            emailid = request.form['email']

            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE users SET name = ?, addr = ?, city = ?, pin = ?, bg = ?, email = ? WHERE email = ?",
                    (name, addr, city, pin, bg, emailid, email)
                )
                conn.commit()
                if email != emailid:
                    session['username'] = emailid  # Update session if email changes
            flash("Profile updated successfully", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "error")
            return redirect(url_for('index'))

@app.route('/contactforblood/<emailid>', methods=['GET', 'POST'])
def contactforblood(emailid):
    if not session.get('username'):
        flash("Please log in to send a request", "error")
        return redirect(url_for('login'))

    try:
        with get_db_connection() as conn:
            if request.method == 'POST':
                fromemail = session['username']
                name = request.form.get('nm', '')
                addr = request.form.get('add', '')

                conn.execute(
                    "INSERT INTO request (toemail, formemail, toname, toaddr) VALUES (?, ?, ?, ?)",
                    (emailid, fromemail, name, addr)
                )
                conn.commit()
                flash("Request sent successfully", "success")
                return redirect(url_for('index'))

            # GET request: Show form or handle directly
            return render_template('contactforblood.html', emailid=emailid)
    except Exception as e:
        flash(f"Error sending request: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/notifications', methods=['GET'])
def notifications():
    if not session.get('username'):
        flash("Please log in to view notifications", "error")
        return redirect(url_for('login'))

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM request WHERE toemail = ?", (session['username'],))
            rows = cur.fetchall()
            if not rows:
                flash("No notifications found", "info")
                return render_template('notifications.html')
            return render_template('notifications.html', rows=rows)
    except sqlite3.OperationalError as e:
        flash(f"Database error: {str(e)}", "error")
        return render_template('notifications.html')
    except Exception as e:
        flash(f"Error fetching notifications: {str(e)}", "error")
        return render_template('notifications.html')

@app.route('/deleteuser/<useremail>', methods=['GET'])
def deleteuser(useremail):
    if not session.get('admin'):
        flash("Admin access required", "error")
        return redirect(url_for('index'))

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE email = ?", (useremail,))
            conn.commit()
            flash(f"Deleted user: {useremail}", "success")
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "error")
        return redirect(url_for('dashboard'))

@app.route('/deletebloodentry/<id>', methods=['GET'])
def deletebloodentry(id):
    if not session.get('admin'):
        flash("Admin access required", "error")
        return redirect(url_for('index'))

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM blood WHERE id = ?", (id,))
            conn.commit()
            flash(f"Deleted blood entry: {id}", "success")
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f"Error deleting blood entry: {str(e)}", "error")
        return redirect(url_for('dashboard'))

@app.route('/deleteme/<useremail>', methods=['GET'])
def deleteme(useremail):
    if session.get('username') != useremail:
        flash("You can only delete your own account", "error")
        return redirect(url_for('index'))

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE email = ?", (useremail,))
            conn.commit()
            session.pop('username', None)
            session.pop('logged_in', None)
            session.pop('admin', None)
            flash(f"Deleted account: {useremail}", "success")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error deleting account: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/deletenoti/<id>', methods=['GET'])
def deletenoti(id):
    if not session.get('username'):
        flash("Please log in to delete notifications", "error")
        return redirect(url_for('login'))

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM request WHERE id = ?", (id,))
            conn.commit()
            flash(f"Deleted notification: {id}", "success")
        return redirect(url_for('notifications'))
    except Exception as e:
        flash(f"Error deleting notification: {str(e)}", "error")
        return redirect(url_for('notifications'))

if __name__ == '__main__':
    app.run(debug=True)