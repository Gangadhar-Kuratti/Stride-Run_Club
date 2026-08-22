from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from database import db

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')

# Authentication decorators
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def index():
    # Get next upcoming run
    next_run = db.fetch_one(
        "SELECT * FROM runs WHERE date >= CURDATE() ORDER BY date ASC, time ASC LIMIT 1"
    )
    
    # Get community statistics
    members_result = db.fetch_one("SELECT COUNT(*) as count FROM members")
    runs_result = db.fetch_one("SELECT COUNT(*) as count FROM runs")
    registrations_result = db.fetch_one("SELECT COUNT(*) as count FROM registrations")
    
    total_members = members_result['count'] if members_result else 0
    total_runs = runs_result['count'] if runs_result else 0
    total_registrations = registrations_result['count'] if registrations_result else 0
    
    stats = {
        'members': total_members,
        'runs': total_runs,
        'registrations': total_registrations
    }
    
    return render_template('index.html', next_run=next_run, stats=stats)

@app.route('/runs')
def runs():
    # Get all upcoming runs
    runs = db.fetch_all(
        "SELECT * FROM runs WHERE date >= CURDATE() ORDER BY date ASC, time ASC"
    )
    
    if not runs:
        runs = []
    
    # Get registration count for each run
    for run in runs:
        count_result = db.fetch_one(
            "SELECT COUNT(*) as count FROM registrations WHERE run_id = %s",
            (run['id'],)
        )
        run['registered_count'] = count_result['count'] if count_result else 0
    
    return render_template('runs.html', runs=runs)

@app.route('/run/<int:run_id>')
def run_details(run_id):
    run = db.fetch_one("SELECT * FROM runs WHERE id = %s", (run_id,))
    
    if not run:
        flash('Run not found.', 'error')
        return redirect(url_for('runs'))
    
    # Get registration count
    count_result = db.fetch_one(
        "SELECT COUNT(*) as count FROM registrations WHERE run_id = %s",
        (run['id'],)
    )
    run['registered_count'] = count_result['count'] if count_result else 0
    
    return render_template('run_details.html', run=run)

@app.route('/join/<int:run_id>')
def join(run_id):
    run = db.fetch_one("SELECT * FROM runs WHERE id = %s", (run_id,))
    
    if not run:
        flash('Run not found.', 'error')
        return redirect(url_for('runs'))
    
    return render_template('join.html', run=run)

@app.route('/register/<int:run_id>', methods=['POST'])
def register_for_run(run_id):
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')
    experience = request.form['experience']
    preferred_distance = request.form['preferred_distance']
    
    # Check if member already exists
    member = db.fetch_one("SELECT * FROM members WHERE email = %s", (email,))
    
    if member:
        member_id = member['id']
    else:
        # Create new member
        cursor = db.execute_query(
            "INSERT INTO members (name, email, phone, experience, preferred_distance) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, experience, preferred_distance)
        )
        member_id = cursor.lastrowid
    
    # Check if already registered for this run
    existing = db.fetch_one(
        "SELECT * FROM registrations WHERE member_id = %s AND run_id = %s",
        (member_id, run_id)
    )
    
    if existing:
        flash('You are already registered for this run.', 'error')
        return redirect(url_for('run_details', run_id=run_id))
    
    # Register for the run
    db.execute_query(
        "INSERT INTO registrations (member_id, run_id) VALUES (%s, %s)",
        (member_id, run_id)
    )
    
    flash('You are in! See you at the run.', 'success')
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Simple admin check (in production, use proper admin table)
        if email == 'admin@stride.com' and password == 'iwilldoit@striderunclub':
            session['admin_id'] = 1
            session['admin_email'] = email
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    # Get statistics
    members_result = db.fetch_one("SELECT COUNT(*) as count FROM members")
    runs_result = db.fetch_one("SELECT COUNT(*) as count FROM runs")
    registrations_result = db.fetch_one("SELECT COUNT(*) as count FROM registrations")
    
    total_members = members_result['count'] if members_result else 0
    total_runs = runs_result['count'] if runs_result else 0
    total_registrations = registrations_result['count'] if registrations_result else 0
    
    stats = {
        'members': total_members,
        'runs': total_runs,
        'registrations': total_registrations
    }
    
    # Get upcoming runs
    runs = db.fetch_all(
        "SELECT * FROM runs WHERE date >= CURDATE() ORDER BY date ASC, time ASC"
    )
    
    if not runs:
        runs = []
    
    # Get recent registrations
    recent_registrations = db.fetch_all("""
        SELECT r.id, m.name, m.email, runs.title, runs.date, r.registered_at
        FROM registrations r
        JOIN members m ON r.member_id = m.id
        JOIN runs ON r.run_id = runs.id
        ORDER BY r.registered_at DESC
        LIMIT 10
    """)
    
    return render_template('admin.html', stats=stats, runs=runs, recent_registrations=recent_registrations)

@app.route('/admin/run/add', methods=['GET', 'POST'])
@login_required
def add_run():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']
        distance = request.form['distance']
        starting_point = request.form['starting_point']
        pace = request.form['pace']
        description = request.form['description']
        
        db.execute_query(
            "INSERT INTO runs (title, date, time, distance, starting_point, pace, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (title, date, time, distance, starting_point, pace, description)
        )
        
        flash('Run added successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('admin.html', add_run_modal=True)

@app.route('/admin/run/edit/<int:run_id>', methods=['GET', 'POST'])
@login_required
def edit_run(run_id):
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']
        distance = request.form['distance']
        starting_point = request.form['starting_point']
        pace = request.form['pace']
        description = request.form['description']
        
        db.execute_query(
            "UPDATE runs SET title = %s, date = %s, time = %s, distance = %s, starting_point = %s, pace = %s, description = %s WHERE id = %s",
            (title, date, time, distance, starting_point, pace, description, run_id)
        )
        
        flash('Run updated successfully!', 'success')
        return redirect(url_for('admin'))
    
    run = db.fetch_one("SELECT * FROM runs WHERE id = %s", (run_id,))
    if not run:
        flash('Run not found.', 'error')
        return redirect(url_for('admin'))
    return render_template('admin.html', edit_run=run)

@app.route('/admin/run/delete/<int:run_id>')
@login_required
def delete_run(run_id):
    db.execute_query("DELETE FROM runs WHERE id = %s", (run_id,))
    flash('Run deleted successfully!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
