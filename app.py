from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smart_college_event_secret_key_tybsc_2026'

# Path to SQLite database file
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')


def get_db():
    """Establishes connection to SQLite database with dictionary cursor."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes database tables and populates sample events and demo users."""
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users Table (Students & Admins)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            roll_no TEXT,
            department TEXT,
            year TEXT,
            phone TEXT,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Events Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            coordinator TEXT NOT NULL,
            coordinator_phone TEXT,
            image_url TEXT,
            max_participants INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Registrations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Confirmed',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            UNIQUE (user_id, event_id)
        )
    ''')

    # Seed Default Administrator if not exists
    cursor.execute("SELECT id FROM users WHERE email = 'admin@college.edu'")
    if not cursor.fetchone():
        admin_pass = generate_password_hash('Admin@123')
        cursor.execute('''
            INSERT INTO users (name, email, password, department, role)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Event Head (Admin)', 'admin@college.edu', admin_pass, 'Computer Science', 'admin'))

    # Seed Default Student if not exists
    cursor.execute("SELECT id FROM users WHERE email = 'student@college.edu'")
    if not cursor.fetchone():
        student_pass = generate_password_hash('Student@123')
        cursor.execute('''
            INSERT INTO users (name, email, password, roll_no, department, year, phone, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('Priya Sharma', 'student@college.edu', student_pass, 'TYCS-101', 'Computer Science', 'TYBSc', '9876543210', 'student'))

    # Seed Sample Events if empty
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        sample_events = [
            (
                'CodeCraft 2026 - Coding Competition',
                'Technical',
                'Annual inter-department competitive coding and debugging challenge. Test your algorithms and problem-solving skills in Python, Java, or C++.',
                '2026-11-15',
                '10:00 AM - 01:00 PM',
                'Computer Lab 3, IT Building',
                'Prof. R. K. Joshi',
                '9820011223',
                'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop&q=80',
                80
            ),
            (
                'Tarang - Annual College Cultural Fest',
                'Cultural',
                'The grand cultural celebration featuring solo singing, group dance, drama, fashion show, and live music band performances.',
                '2026-11-20',
                '09:00 AM - 05:00 PM',
                'Main College Auditorium',
                'Dr. Anita Nair',
                '9820044556',
                'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600&auto=format&fit=crop&q=80',
                300
            ),
            (
                'Rann - Inter-Department Sports Meet',
                'Sports',
                'Thrilling sports tournament covering box cricket, football, badminton, chess, and athletic sprints. Trophies for champion department!',
                '2026-11-25',
                '08:00 AM - 04:00 PM',
                'College Sports Ground',
                'Coach Sunil Patil',
                '9820077889',
                'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop&q=80',
                200
            ),
            (
                'TechVision: Seminar on AI & Cloud Computing',
                'Technical Seminar',
                'Expert tech talk by industry senior architects from leading IT firms on Generative AI, cloud infrastructure, and modern software careers.',
                '2026-12-02',
                '11:00 AM - 01:30 PM',
                'Seminar Hall A, Science Wing',
                'Prof. Neha Kulkarni',
                '9820099001',
                'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&auto=format&fit=crop&q=80',
                120
            ),
            (
                'InnovateX: TYBSc Computer Science Project Exhibition',
                'Exhibition',
                'Final year software project showcase, working website demos, poster evaluations, and interaction with alumni tech judges.',
                '2026-12-10',
                '10:00 AM - 04:00 PM',
                'Central Exhibition Hall',
                'Dr. M. S. Deshmukh',
                '9820033445',
                'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&auto=format&fit=crop&q=80',
                150
            )
        ]
        cursor.executemany('''
            INSERT INTO events (title, category, description, date, time, venue, coordinator, coordinator_phone, image_url, max_participants)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_events)

    conn.commit()
    conn.close()


# Decorators for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in as Administrator.', 'warning')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Access denied! Administrator privileges required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------- PUBLIC ROUTES -------------------

@app.route('/')
def home():
    """Home page with hero banner, statistics, and featured upcoming events."""
    conn = get_db()
    cursor = conn.cursor()

    # Fetch 3 latest upcoming events
    cursor.execute("SELECT * FROM events ORDER BY date ASC LIMIT 3")
    featured_events = cursor.fetchall()

    # System counts for live counters
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total_registrations = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'index.html',
        events=featured_events,
        total_events=total_events,
        total_students=total_students,
        total_registrations=total_registrations
    )


@app.route('/about')
def about():
    """About us page explaining event committee objectives and student participation."""
    return render_template('about.html')


@app.route('/events')
def events():
    """List of all college events with search by title and filter by category."""
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if search_query:
        query += " AND title LIKE ?"
        params.append(f"%{search_query}%")

    if category_filter:
        query += " AND category = ?"
        params.append(category_filter)

    query += " ORDER BY date ASC"

    cursor.execute(query, params)
    all_events = cursor.fetchall()

    # Get distinct categories for filter buttons
    cursor.execute("SELECT DISTINCT category FROM events")
    categories = [row['category'] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        'events.html',
        events=all_events,
        categories=categories,
        search_query=search_query,
        selected_category=category_filter
    )


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Detailed view for an event with coordinator info and registration status."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    if not event:
        conn.close()
        flash('Event not found.', 'danger')
        return redirect(url_for('events'))

    # Count registered participants
    cursor.execute("SELECT COUNT(*) FROM registrations WHERE event_id = ?", (event_id,))
    registered_count = cursor.fetchone()[0]

    # Check if current logged in user has already registered
    already_registered = False
    if 'user_id' in session:
        cursor.execute(
            "SELECT id FROM registrations WHERE user_id = ? AND event_id = ?",
            (session['user_id'], event_id)
        )
        if cursor.fetchone():
            already_registered = True

    conn.close()

    return render_template(
        'event_detail.html',
        event=event,
        registered_count=registered_count,
        already_registered=already_registered
    )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with inquiries submission."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        flash(f'Thank you, {name}! Your message regarding "{subject}" has been received. Our event committee will get back to you.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


# ------------------- AUTHENTICATION ROUTES -------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page."""
    if 'user_id' in session:
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        roll_no = request.form.get('roll_no', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        phone = request.form.get('phone', '').strip()

        if not name or not email or not password:
            flash('Name, Email, and Password are required!', 'danger')
            return redirect(url_for('register'))

        conn = get_db()
        cursor = conn.cursor()

        # Check existing email
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            flash('An account with this email already exists. Please log in.', 'warning')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, roll_no, department, year, phone, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'student')
            ''', (name, email, hashed_password, roll_no, department, year, phone))
            conn.commit()

            # Auto log in the student
            user_id = cursor.lastrowid
            session['user_id'] = user_id
            session['user_name'] = name
            session['user_email'] = email
            session['user_role'] = 'student'

            flash(f'Registration successful! Welcome to the Event Portal, {name}.', 'success')
            conn.close()
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            conn.close()
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page for both Students and Admins."""
    if 'user_id' in session:
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']

            flash(f'Welcome back, {user["name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logs user out and destroys session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ------------------- STUDENT MODULE -------------------

@app.route('/event/<int:event_id>/register', methods=['POST'])
@login_required
def register_for_event(event_id):
    """Registers the logged-in student for a selected event."""
    if session.get('user_role') == 'admin':
        flash('Administrators cannot register for events as students.', 'info')
        return redirect(url_for('event_detail', event_id=event_id))

    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()

    # Check if event exists
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    if not event:
        conn.close()
        flash('Event does not exist.', 'danger')
        return redirect(url_for('events'))

    # Check for duplicate registration
    cursor.execute("SELECT id FROM registrations WHERE user_id = ? AND event_id = ?", (user_id, event_id))
    if cursor.fetchone():
        conn.close()
        flash('You are already registered for this event!', 'warning')
        return redirect(url_for('event_detail', event_id=event_id))

    # Check max capacity
    cursor.execute("SELECT COUNT(*) FROM registrations WHERE event_id = ?", (event_id,))
    current_count = cursor.fetchone()[0]
    if current_count >= event['max_participants']:
        conn.close()
        flash('Sorry! Registrations for this event are full.', 'danger')
        return redirect(url_for('event_detail', event_id=event_id))

    # Insert registration
    cursor.execute(
        "INSERT INTO registrations (user_id, event_id, status) VALUES (?, ?, 'Confirmed')",
        (user_id, event_id)
    )
    conn.commit()
    conn.close()

    flash(f'Congratulations! You have successfully registered for "{event["title"]}".', 'success')
    return redirect(url_for('student_dashboard'))


@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student dashboard displaying profile and list of registered events."""
    user_id = session['user_id']

    conn = get_db()
    cursor = conn.cursor()

    # Fetch user details
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    student = cursor.fetchone()

    # Fetch registered events
    cursor.execute('''
        SELECT r.id as reg_id, r.registered_at, r.status,
               e.id as event_id, e.title, e.category, e.date, e.time, e.venue, e.coordinator
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        WHERE r.user_id = ?
        ORDER BY r.registered_at DESC
    ''', (user_id,))
    my_registrations = cursor.fetchall()

    conn.close()

    return render_template(
        'student_dashboard.html',
        student=student,
        registrations=my_registrations
    )


@app.route('/student/cancel-registration/<int:reg_id>', methods=['POST'])
@login_required
def cancel_registration(reg_id):
    """Allows student to cancel their event registration."""
    user_id = session['user_id']

    conn = get_db()
    cursor = conn.cursor()

    # Verify ownership
    cursor.execute("SELECT id FROM registrations WHERE id = ? AND user_id = ?", (reg_id, user_id))
    registration = cursor.fetchone()

    if not registration:
        conn.close()
        flash('Registration record not found or access denied.', 'danger')
        return redirect(url_for('student_dashboard'))

    cursor.execute("DELETE FROM registrations WHERE id = ?", (reg_id,))
    conn.commit()
    conn.close()

    flash('Event registration cancelled successfully.', 'success')
    return redirect(url_for('student_dashboard'))


# ------------------- ADMIN MODULE -------------------

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard showing overall stats, all events, and recent registrations."""
    conn = get_db()
    cursor = conn.cursor()

    # Counts
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total_registrations = cursor.fetchone()[0]

    # All events list with registered counts
    cursor.execute('''
        SELECT e.*, COUNT(r.id) as reg_count
        FROM events e
        LEFT JOIN registrations r ON e.id = r.event_id
        GROUP BY e.id
        ORDER BY e.date ASC
    ''')
    events_list = cursor.fetchall()

    # Recent 10 registrations
    cursor.execute('''
        SELECT r.id, r.registered_at, u.name as student_name, u.email as student_email,
               u.roll_no, u.department, e.title as event_title
        FROM registrations r
        JOIN users u ON r.user_id = u.id
        JOIN events e ON r.event_id = e.id
        ORDER BY r.registered_at DESC
        LIMIT 10
    ''')
    recent_registrations = cursor.fetchall()

    conn.close()

    return render_template(
        'admin_dashboard.html',
        total_events=total_events,
        total_students=total_students,
        total_registrations=total_registrations,
        events=events_list,
        recent_registrations=recent_registrations
    )


@app.route('/admin/add-event', methods=['GET', 'POST'])
@admin_required
def add_event():
    """Admin page to create a new college event."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        venue = request.form.get('venue', '').strip()
        coordinator = request.form.get('coordinator', '').strip()
        coordinator_phone = request.form.get('coordinator_phone', '').strip()
        image_url = request.form.get('image_url', '').strip()
        max_participants = int(request.form.get('max_participants', 100) or 100)

        if not title or not category or not date or not venue:
            flash('Please fill in all mandatory event fields.', 'danger')
            return redirect(url_for('add_event'))

        if not image_url:
            image_url = 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=600&auto=format&fit=crop&q=80'

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (title, category, description, date, time, venue, coordinator, coordinator_phone, image_url, max_participants)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, category, description, date, time, venue, coordinator, coordinator_phone, image_url, max_participants))
        conn.commit()
        conn.close()

        flash(f'Event "{title}" created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_event.html')


@app.route('/admin/edit-event/<int:event_id>', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    """Admin page to modify existing event details."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    if not event:
        conn.close()
        flash('Event not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        venue = request.form.get('venue', '').strip()
        coordinator = request.form.get('coordinator', '').strip()
        coordinator_phone = request.form.get('coordinator_phone', '').strip()
        image_url = request.form.get('image_url', '').strip()
        max_participants = int(request.form.get('max_participants', 100) or 100)

        cursor.execute('''
            UPDATE events
            SET title = ?, category = ?, description = ?, date = ?, time = ?, venue = ?,
                coordinator = ?, coordinator_phone = ?, image_url = ?, max_participants = ?
            WHERE id = ?
        ''', (title, category, description, date, time, venue, coordinator, coordinator_phone, image_url, max_participants, event_id))
        conn.commit()
        conn.close()

        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    conn.close()
    return render_template('edit_event.html', event=event)


@app.route('/admin/delete-event/<int:event_id>', methods=['POST'])
@admin_required
def delete_event(event_id):
    """Admin deletes an event and its associated registrations."""
    conn = get_db()
    cursor = conn.cursor()

    # Delete related registrations first
    cursor.execute("DELETE FROM registrations WHERE event_id = ?", (event_id,))
    # Delete the event
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))

    conn.commit()
    conn.close()

    flash('Event and its registrations deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/event/<int:event_id>/registrations')
@admin_required
def event_registrations(event_id):
    """Admin views list of students registered for a specific event."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    if not event:
        conn.close()
        flash('Event not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    cursor.execute('''
        SELECT r.id as reg_id, r.registered_at, r.status,
               u.name, u.email, u.roll_no, u.department, u.year, u.phone
        FROM registrations r
        JOIN users u ON r.user_id = u.id
        WHERE r.event_id = ?
        ORDER BY r.registered_at ASC
    ''', (event_id,))
    students = cursor.fetchall()

    conn.close()

    return render_template(
        'event_registrations.html',
        event=event,
        students=students,
        total_count=len(students)
    )


# Run application
if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("[OK] Smart Event Management System is Running!")
    print("[URL] Local Access: http://127.0.0.1:5000")
    print("[LOGIN] Admin:   admin@college.edu   / Admin@123")
    print("[LOGIN] Student: student@college.edu / Student@123")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
