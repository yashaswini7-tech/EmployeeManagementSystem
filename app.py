from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "employee-management-secret-key-change-this"

DATABASE = "database.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Admin'
        )
    """)

    # Employees table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            date_joined TEXT NOT NULL
        )
    """)

    # Create default admin account
    existing_user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if not existing_user:
        hashed_password = generate_password_hash("admin123")

        conn.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            ("admin", hashed_password, "Admin")
        )

    conn.commit()
    conn.close()


# ============================================================
# AUTHENTICATION DECORATOR
# ============================================================

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return decorated_function


# ============================================================
# LOGIN
# ============================================================

@app.route("/", methods=["GET", "POST"])
def login():

    # If already logged in
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "info")

    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db()

    total_employees = conn.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    total_departments = conn.execute(
        "SELECT COUNT(DISTINCT department) FROM employees"
    ).fetchone()[0]

    average_salary = conn.execute(
        "SELECT AVG(salary) FROM employees"
    ).fetchone()[0]

    recent_employees = conn.execute(
        """
        SELECT *
        FROM employees
        ORDER BY id DESC
        LIMIT 5
        """
    ).fetchall()

    conn.close()

    if average_salary is None:
        average_salary = 0

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        total_departments=total_departments,
        average_salary=average_salary,
        recent_employees=recent_employees
    )


# ============================================================
# EMPLOYEES - READ
# ============================================================

@app.route("/employees")
@login_required
def employees():

    search = request.args.get("search", "")
    department = request.args.get("department", "")

    conn = get_db()

    query = "SELECT * FROM employees WHERE 1=1"
    parameters = []

    # Search
    if search:

        query += """
            AND (
                name LIKE ?
                OR email LIKE ?
                OR position LIKE ?
            )
        """

        search_value = f"%{search}%"

        parameters.extend([
            search_value,
            search_value,
            search_value
        ])

    # Department filter
    if department:

        query += " AND department = ?"

        parameters.append(department)

    query += " ORDER BY id DESC"

    employees_list = conn.execute(
        query,
        parameters
    ).fetchall()

    departments = conn.execute(
        "SELECT DISTINCT department FROM employees ORDER BY department"
    ).fetchall()

    conn.close()

    return render_template(
        "employees.html",
        employees=employees_list,
        departments=departments,
        search=search,
        selected_department=department
    )


# ============================================================
# ADD EMPLOYEE - CREATE
# ============================================================

@app.route("/employees/add", methods=["GET", "POST"])
@login_required
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        position = request.form["position"]
        salary = request.form["salary"]
        date_joined = request.form["date_joined"]

        conn = get_db()

        try:

            conn.execute(
                """
                INSERT INTO employees
                (name, email, phone, department, position, salary, date_joined)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    phone,
                    department,
                    position,
                    salary,
                    date_joined
                )
            )

            conn.commit()

            flash("Employee added successfully!", "success")

            return redirect(url_for("employees"))

        except sqlite3.IntegrityError:

            flash("An employee with this email already exists.", "danger")

        finally:

            conn.close()

    return render_template("add_employee.html")


# ============================================================
# EDIT EMPLOYEE - UPDATE
# ============================================================

@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_employee(id):

    conn = get_db()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (id,)
    ).fetchone()

    if not employee:

        conn.close()

        flash("Employee not found.", "danger")

        return redirect(url_for("employees"))

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        position = request.form["position"]
        salary = request.form["salary"]
        date_joined = request.form["date_joined"]

        try:

            conn.execute(
                """
                UPDATE employees
                SET
                    name = ?,
                    email = ?,
                    phone = ?,
                    department = ?,
                    position = ?,
                    salary = ?,
                    date_joined = ?
                WHERE id = ?
                """,
                (
                    name,
                    email,
                    phone,
                    department,
                    position,
                    salary,
                    date_joined,
                    id
                )
            )

            conn.commit()

            flash("Employee updated successfully!", "success")

            conn.close()

            return redirect(url_for("employees"))

        except sqlite3.IntegrityError:

            flash(
                "Another employee already uses this email.",
                "danger"
            )

    conn.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )


# ============================================================
# DELETE EMPLOYEE - DELETE
# ============================================================

@app.route("/employees/delete/<int:id>", methods=["POST"])
@login_required
def delete_employee(id):

    conn = get_db()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (id,)
    ).fetchone()

    if employee:

        conn.execute(
            "DELETE FROM employees WHERE id = ?",
            (id,)
        )

        conn.commit()

        flash("Employee deleted successfully.", "success")

    else:

        flash("Employee not found.", "danger")

    conn.close()

    return redirect(url_for("employees"))


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )