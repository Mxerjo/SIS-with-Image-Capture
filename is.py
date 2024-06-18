from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
import mysql.connector
import os

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure 'uploads' directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'project_db',
}

def allowed_file(filename):
    # Check if the file has an allowed extension
    allowed_extensions = {'png', 'jpeg', 'jpg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def connect_db():
    return mysql.connector.connect(**db_config)

def insert_data(first_name, middle_name, last_name, contact, gender, birth_date, course,
                institutional_email, student_number, password, photo_path):
    conn = connect_db()
    cursor = conn.cursor()

    # Extract the file name from the photo_path
    photo_filename = os.path.basename(photo_path)

    # Specify column names in the INSERT statement
    cursor.execute('''
        INSERT INTO student_tbl (first_name, middle_name, last_name, contact, gender, birth_date, course,
                   institutional_email, student_number, password, photo_path, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (first_name, middle_name, last_name, contact, gender, birth_date, course,
          institutional_email, student_number, password, photo_filename, 'active'))
    conn.commit()
    conn.close()

def get_all_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_tbl")
    flask_data = cursor.fetchall()
    conn.close()
    print(flask_data) 
    return flask_data

# Registration route
@app.route("/registration")
def registration():
    return render_template('user_form.html')

# Form submission route
@app.route("/form", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Extracting form data
        first_name = request.form['fname']
        middle_name = request.form['midname']
        last_name = request.form['lname']
        contact = request.form['tel']
        gender = request.form['gen']
        birth_date = request.form['bdate']
        course = request.form['crsename']
        institutional_email = request.form['mail']
        student_number = request.form['studnum']
        password = request.form['pass']

        # Check if the student number already exists
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_tbl WHERE student_number = %s", (student_number,))
        existing_student = cursor.fetchone()
        conn.close()

        if existing_student:
            # If a matching record is found, display an error message or handle it as needed
            return render_template('user_form.html', error_existing="Student number already exists.")

        # Handle file upload
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '' and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
            else:
                return render_template('user_form.html', error_invalid="Invalid file type. Please choose another file.")
            
        # Insert data into the database
        insert_data(first_name, middle_name, last_name, contact, gender, birth_date, course,
                    institutional_email, student_number, password, filename)

    # Fetch all data and render the user login page
    flask_data = get_all_data()
    return render_template('user_login.html', htmldata=flask_data)

@app.route("/edit/<int:student_id>", methods=['GET', 'POST'])
def edit_page(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Fetch user data based on student_id
        cursor.execute("SELECT * FROM student_tbl WHERE student_id = %s", (student_id,))
        studentdata = cursor.fetchone()

        if studentdata:
            student_data = {
                'student_id': studentdata[0],
                'first_name': studentdata[1],
                'middle_name': studentdata[2],
                'last_name': studentdata[3],
                'contact': studentdata[4],
                'gender': studentdata[5],
                'birth_date': studentdata[6],
                'institutional_email': studentdata[7],
                'course': studentdata[8],
                'student_number': studentdata[9],
                'password': studentdata[10],
                'photo_path': studentdata[11]
            }
            return render_template('user_edit.html', studentdata=student_data)
        else:
            return render_template('user_home.html', message="User not found")

    elif request.method == 'POST':
        # Update user data
        first_name = request.form['fname']
        middle_name = request.form['midname']
        last_name = request.form['lname']
        contact = request.form['tel']
        gender = request.form['gen']
        birth_date = request.form['bdate']
        institutional_email = request.form['mail']
        course = request.form['cname']
        student_number = request.form['studnum']
        password = request.form['pass']

        cursor.execute('''
            UPDATE student_tbl SET first_name=%s, middle_name=%s, last_name=%s, contact=%s,
            gender=%s, birth_date=%s, course=%s, institutional_email=%s, student_number=%s,
            password=%s WHERE student_id=%s
        ''', (first_name, middle_name, last_name, contact, gender, birth_date, course,
              institutional_email, student_number, password, student_id))
        conn.commit()
        conn.close()

       # Redirect to the user home page or any other page
        return redirect(url_for('loginuser'))  # Change 'user_home' to the actual route

    conn.close()

# Login page route
@app.route("/login")
def log():
    return render_template('user_login.html')

# User login route
@app.route("/userlogin", methods=["POST", "GET"])
def loginuser():
    if request.method == 'POST':
        student_number = request.form.get('studnum')
        password = request.form.get('pass')

        # You need to query the database to check if the provided credentials are valid
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_tbl WHERE student_number = %s AND password = %s", (student_number, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Check the account status
            # Use the correct index for the 'status' field
            if user[12] == 'inactive':  # Make sure 'status' is at the correct index
                # If the account is inactive, render an error message or redirect to the login page
                return render_template('user_login.html', error="Account is Deactivate.")
            
            # Successful login, display the details of the logged-in user
            user_data = {
                'student_id': user[0],
                'first_name': user[1],
                'middle_name': user[2],
                'last_name': user[3],
                'contact': user[4],
                'gender': user[5],
                'birth_date': user[6],
                'institutional_email': user[7],
                'course': user[8],
                'student_number': user[9],
                'password': user[10],
                'photo_path': user[11], 
            }
            # Successful login, you can redirect to a new page or do something else
            return render_template('user_home.html', user=user_data)
        else:
            # Failed login, you can render an error message or redirect to the login page
            return render_template('user_login.html', error="Invalid credentials")

    # If the request method is GET, render the login form
    return render_template('user_login.html')

# Admin login route
@app.route("/admin")
def adminlog():
    return render_template('admin_login.html')

# Admin login validation route
@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == 'POST':
        user_name = request.form.get('adname')
        password = request.form.get('adpass')

        # You need to query the database to check if the provided credentials are valid
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_tbl WHERE user_name = %s AND password = %s", (user_name, password))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM student_tbl")
        students = cursor.fetchall()

        conn.close()

        if user:
            return render_template('admin_display.html', students=students)
        else:
            # Failed login, you can render an error message or redirect to the login page
            return render_template('admin_login.html', error="Invalid credentials")

    # If the request method is GET, render the login form
    return render_template('admin_login.html')

# Search students route
@app.route("/search", methods=["POST"])
def search_students():
    # Get the search query from the form
    search_query = request.form.get('search')

    # You need to query the database to get the results based on the search query
    conn = connect_db()
    cursor = conn.cursor()

    if search_query:
        # Filter by student number when a search query is present
        cursor.execute("SELECT * FROM student_tbl WHERE student_number = %s", (search_query,))
    else:
        cursor.execute("SELECT * FROM student_tbl")

    students = cursor.fetchall()

    conn.close()

    # Render the template with the search results
    return render_template('admin_display.html', students=students)

# Back Button to View
@app.route("/admin/dashboard")
def view_button():
    return render_template('admin_display.html')

# View student details route
@app.route("/view/<int:student_id>")
def view_student(student_id):
    # You need to query the database to get the details of the selected student
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_tbl WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if student:
        # Render the template with the student details
        student_data = {
            'student_id': student[0],
            'first_name': student[1],
            'middle_name': student[2],
            'last_name': student[3],
            'contact': student[4],
            'gender': student[5],
            'birth_date': student[6],
            'institutional_email': student[7],
            'course': student[8],
            'student_number': student[9],
            'password': student[10],
            'photo_path': student[11],
        }
        return render_template('admin_view.html', student=student_data)
    else:
        # Handle the case where the student is not found
        flash("Student not found", "error")
        return redirect(url_for('adminlogin'))
    
# Deactivate student route
@app.route("/deactivate/<int:student_id>", methods=["POST"])
def deactivate_student(student_id):
    # You need to query the database to update the status of the selected student
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE student_tbl SET status = 'inactive' WHERE student_id = %s", (student_id,))
    conn.commit()
    conn.close()

    # Redirect back to the admin display page
    return redirect(url_for('view_student', student_id=student_id))

# Activate student route
@app.route("/activate/<int:student_id>", methods=["POST"])
def activate_student(student_id):
    # You need to query the database to update the status of the selected student
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE student_tbl SET status = 'active' WHERE student_id = %s", (student_id,))
    conn.commit()
    conn.close()

    # Redirect back to the admin display page
    return redirect(url_for('view_student', student_id=student_id))

# Logout route
@app.route("/logout")
def logout():
     # Redirect to the login page
    return redirect(url_for('log')) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
