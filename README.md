# Smart Event Management System of College
**A Mini Project for TYBSc Computer Science**

---

## 1. Project Introduction

The **Smart Event Management System** is a complete, lightweight, and responsive web application designed for colleges and universities to automate the planning, announcement, registration, and attendance tracking of campus events.

Built with **Python Flask**, **SQLite**, and **Bootstrap 5**, it provides an intuitive digital hub where students can discover upcoming events, check venue and coordinator details, and register online with instant digital participation passes. Simultaneously, faculty coordinators and college administrators can schedule events, view attendee lists, and track campus engagement metrics.

---

## 2. Problem Statement

In many traditional college environments:
- Event notices are scattered across physical bulletin boards, classroom announcements, or informal WhatsApp groups.
- Student registrations rely on manual paperwork, physical sign-up desks, or unstructured Google Forms.
- Duplicate registrations cause confusion, inflated participant counts, and seat-wasting in competitive events.
- Faculty coordinators spend substantial manual effort compiling attendee rosters and verifying student eligibility.

The **Smart Event Management System** solves these challenges by providing a centralized, automated, and tamper-resistant digital registration platform.

---

## 3. Project Objectives

1. **Centralize Event Discovery:** Provide a single calendar view for all technical competitions, cultural fests, sports meets, seminars, and exhibitions.
2. **Prevent Duplicate Registrations:** Automatically validate database records so students cannot register more than once for the same event.
3. **Streamline Administration:** Allow administrators to add, update, and delete events and monitor real-time participant counts.
4. **Instant Digital Entry Passes:** Enable students to generate and print verified participation slips directly from their personal dashboard.
5. **Ensure Security & Accessibility:** Implement password hashing (Werkzeug) and role-based access decorators to secure administrative operations.

---

## 4. Software & Hardware Requirements

### Software Requirements:
- **Operating System:** Windows 10/11, macOS, or Linux
- **Programming Language:** Python 3.8+ (Tested on Python 3.13)
- **Web Framework:** Flask 3.0+
- **Database:** SQLite (Embedded, pre-installed with Python)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 (via CDN), Bootstrap Icons

### Hardware Requirements:
- **Processor:** Dual Core 1.5 GHz or higher
- **RAM:** 2 GB minimum (4 GB recommended)
- **Hard Disk Space:** 100 MB free space

---

## 5. Main Modules

### 1. Public & Student Portal:
- **Home Page:** Hero banner, live event counters, featured upcoming competitions, and participation benefits.
- **About Us:** Information about the college event cell and project scope.
- **Event Catalog:** Search events by name and filter by category (Technical, Cultural, Sports, Seminars, Exhibitions).
- **Event Details:** Full event schedule, venue, faculty coordinator contact, capacity tracking, and one-click registration.
- **Student Dashboard:** Personal profile overview, list of registered events, registration status, cancellation options, and printable event entry pass modal.
- **Contact Us:** Interactive inquiry form to reach the event committee.

### 2. Administrator Portal:
- **Admin Dashboard:** Statistical counters (Total Events, Registered Students, Total Registrations).
- **Event Management (CRUD):** Add new events, edit existing event parameters, and delete events with automatic cascading registration cleanup.
- **Attendance Roster:** Dedicated view of all registered students for any specific event with a printable attendance sheet for judges and coordinators.

---

## 6. Database Design

The system uses SQLite (`database.db`), which is automatically created and populated upon the first launch:

### 1. Table: `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `name` | TEXT | NOT NULL | Student or admin full name |
| `email` | TEXT | UNIQUE NOT NULL | College email address |
| `password` | TEXT | NOT NULL | Securely hashed password |
| `roll_no` | TEXT | NULLABLE | College Roll Number (e.g. TYCS-101) |
| `department` | TEXT | NULLABLE | Department/Branch |
| `year` | TEXT | NULLABLE | Academic Year (FY, SY, TYBSc) |
| `phone` | TEXT | NULLABLE | Contact telephone |
| `role` | TEXT | DEFAULT 'student' | User role (`student` or `admin`) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

### 2. Table: `events`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique event identifier |
| `title` | TEXT | NOT NULL | Event title |
| `category` | TEXT | NOT NULL | Category (Technical, Cultural, Sports, etc.) |
| `description` | TEXT | NOT NULL | Full event rules and schedule |
| `date` | TEXT | NOT NULL | Scheduled event date (YYYY-MM-DD) |
| `time` | TEXT | NOT NULL | Scheduled time slot |
| `venue` | TEXT | NOT NULL | Campus location or hall |
| `coordinator` | TEXT | NOT NULL | Faculty coordinator name |
| `coordinator_phone` | TEXT | NULLABLE | Coordinator contact number |
| `image_url` | TEXT | NULLABLE | Banner image link |
| `max_participants` | INTEGER | DEFAULT 100 | Seat / participant capacity limit |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Posting timestamp |

### 3. Table: `registrations`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Registration record ID |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Registered student ID |
| `event_id` | INTEGER | FOREIGN KEY (`events.id`) | Target event ID |
| `registered_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |
| `status` | TEXT | DEFAULT 'Confirmed' | Registration status |
| *Constraint* | UNIQUE (`user_id`, `event_id`) | **Prevents duplicate registrations** |

---

## 7. How to Install and Run Locally (Windows)

### Step 1: Open Terminal / PowerShell
Navigate to the project directory:
```powershell
cd "c:\AGRO MARKET\smart-event-management-system"
```

### Step 2: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Start the Flask Application
```powershell
python app.py
```

### Step 4: Access in Your Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 8. Pre-Seeded Demo Login Credentials

For demonstration and viva presentation, the system is pre-configured with two ready-to-use accounts:

| Role | Email | Password | Access Rights |
|---|---|---|---|
| **Administrator** | `admin@college.edu` | `Admin@123` | Full access to add/edit/delete events and view participant rosters |
| **Student** | `student@college.edu` | `Student@123` | Register for events, view entry passes, cancel registrations |

*(Note: On the login page, you can also click the "Demo Credentials" buttons to auto-fill the login fields instantly!)*

---

## 9. How to Run the Automated Test Suite

To verify that all routes, authentication checks, and duplicate registration guards are working properly, run:
```powershell
python test_app.py
```
Expected output:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.900s

OK
```

---

## 10. How to Deploy the Website for Free Online

To get a public URL for your project demonstration:

### Method A: Deploy on Render (Recommended & Free)
1. Initialize a Git repository in `smart-event-management-system`:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Smart Event Management System"
   ```
2. Push your project to a public or private GitHub repository.
3. Sign up at [Render.com](https://render.com).
4. Click **New +** > **Web Service**.
5. Connect your GitHub repository.
6. Configure the settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
7. Click **Deploy Web Service**.
8. Render will deploy your application and give you a free public URL (e.g., `https://smart-college-events.onrender.com`).

### Method B: Deploy on PythonAnywhere (100% Free for Flask)
1. Sign up for a free beginner account at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. In the **Web** tab, click **Add a new web app** and choose **Flask** with **Python 3.10+**.
3. Upload your files (`app.py`, `templates/`, `static/`) using the **Files** tab or clone via Git.
4. Reload the web app. Your site will be live at `https://<your-username>.pythonanywhere.com`.

---

## 11. Conclusion

The **Smart Event Management System of College** replaces fragmented, paper-based event workflows with an automated, responsive, and secure platform. It simplifies student participation, guarantees data integrity by preventing duplicate registrations, and gives administrators clear insights into campus engagement.

---

## 12. 10 Viva Questions and Answers for TYBSc Students

**Q1: What is the primary purpose of this project?**  
*Answer:* To automate the organization, announcement, and student registration process for college events, eliminating manual paperwork and preventing duplicate registrations.

**Q2: Why did you choose Python Flask for the backend?**  
*Answer:* Flask is a lightweight WSGI microframework that is beginner-friendly, modular, and does not impose rigid boilerplate, making it ideal for demonstrating full-stack fundamentals.

**Q3: Which database did you use and why?**  
*Answer:* SQLite. It is an embedded relational database engine that requires zero configuration, stores data in a single file (`database.db`), and supports standard SQL queries and constraints.

**Q4: How did you prevent a student from registering twice for the same event?**  
*Answer:* At the database level, a `UNIQUE (user_id, event_id)` constraint is placed on the `registrations` table. At the application level, Flask queries the database prior to insertion; if a record exists, a warning is returned and registration is rejected.

**Q5: How is user password security handled?**  
*Answer:* Passwords are never stored in plaintext. We use Werkzeug's `generate_password_hash()` (using PBKDF2/SHA256) upon registration and `check_password_hash()` during login.

**Q6: What is a Flask session and what data is stored in it?**  
*Answer:* A Flask session stores client-specific information across requests using cryptographically signed cookies. We store `user_id`, `user_name`, `user_email`, and `user_role` to maintain login state.

**Q7: How did you protect administrator pages from student access?**  
*Answer:* We implemented a custom Python decorator `@admin_required` that checks if the logged-in user's role is `'admin'`. If a student or unauthenticated visitor attempts to access an admin URL, access is denied and they are redirected.

**Q8: What front-end technologies did you use for the UI design?**  
*Answer:* HTML5 for semantic structure, CSS3 with a blue-and-white theme, JavaScript for alert timeouts and confirmations, and Bootstrap 5 for responsive grid cards and mobile navigation.

**Q9: What happens when an administrator deletes an event?**  
*Answer:* To maintain referential integrity, the backend deletes all associated entries in the `registrations` table for that event first, and then deletes the event record from the `events` table.

**Q10: What future enhancements can be added to this system?**  
*Answer:* Automatic QR-code scanning for on-site venue attendance, automated email/SMS confirmation reminders, and online payment gateway integration for paid events or workshops.
