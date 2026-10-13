# EmployeeManagementSystem
A web-based Employee Management System developed using Python Flask, SQLite, HTML, CSS and Bootstrap.

## Project Overview

The Employee Management System is a web-based application developed to manage employee information efficiently. It allows an authorized user to add, view, update, search, filter and delete employee records.

The project demonstrates the integration of a Python Flask backend with a PostgreSQL database and a responsive frontend.

## Objectives

- Store employee information in a structured database.
- Provide login authentication for users.
- Perform CRUD operations on employee records.
- Search employees and filter them by department.
- Display employee statistics on a dashboard.

## Technologies Used

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python, Flask
- **Database:** SQLite
- **Database Connector:** Psycopg2
- **Authentication:** Flask sessions and Werkzeug password hashing

## Features

1. Login and logout functionality
2. Employee dashboard
3. Add new employee records
4. View all employees
5. Edit employee details
6. Delete employee records
7. Search employees by name, email or position
8. Filter employees by department
9. View total employees, departments and average salary

## Project Structure

```text
employee-management-system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── add_employee.html
│   └── edit_employee.html
└── static/
    └── style.css
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd employee-management-system
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open pgAdmin or PostgreSQL's SQL Shell and execute:

```sql
CREATE DATABASE employee_management;
```

### 5. Configure the database

Set the PostgreSQL database name, username, password, host and port in the application's configuration. Keep database passwords out of the repository.

### 6. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Database Tables

### Users
Stores user login information and roles.

### Employees
Stores employee names, email addresses, phone numbers, departments, positions, salaries and joining dates.

## Learning Outcomes

- Understanding Flask routes and templates
- Connecting Python applications to PostgreSQL
- Performing SQL CRUD operations
- Implementing basic login authentication
- Organizing a web development project using GitHub

## Future Enhancements

- Role-based access control
- Employee profile photographs
- Pagination and export to CSV
- Improved input validation and security
- Deployment to a cloud hosting platform

## Author

Add your name here.

## Project Status

Academic project — development version.
