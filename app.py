from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import subprocess
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os



app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'


# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_mongo_login_registration']
users_collection = db['users']
#edit
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy user data for demonstration purposes
# users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/h')
def home1():
    return render_template('home1.html')

@app.route('/tutorial')
def tutorials():
    return render_template('tutorials.html')
@app.route('/tutor')
def tutor():
    return render_template('tutorials1.html')

@app.route('/exercise')
def exercises():
    return render_template('exercises.html')

@app.route('/resource')
def resources():
    return render_template('resources.html')
@app.route('/resource1')
def resources1():
    return render_template('resources1.html')

@app.route('/project')
def projects():
    return render_template('projects.html')

# @app.route('/tutorial/login')
# def tut_login():
#     return render_page('login',url_for('login_page'))

# @app.route('/tutorial/login')
# def login_page():
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        radio_option = request.form.get('radio')
        user = users_collection.find_one({'username': username})
        
        if user and user['password'] == password and user['radio'] == radio_option:
            if radio_option=="radio1":
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home1'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        radio_option = request.form.get('radio')
        existing_user = users_collection.find_one({'username': username})

        if existing_user:
            return render_template('login.html', error='Username already exists. Choose another username')
        else:
            users_collection.insert_one({'username': username, 'password': password,'radio': radio_option})
            return render_template('login.html', message='Registration successful! Please log in.')

    return render_template('register.html')

@app.route('/compiler')
def compiler():
    return render_template('compiler.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.form['code']
    result = compile_and_run_code(code)
    return result

def compile_and_run_code(code):
    # This is a basic example; you may need to adjust it based on your specific requirements
    try:
        result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output


@app.route('/edit')
def edit():
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('edit.html', filenames=filenames)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('edit'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download1')
def downloads():
    return render_template('downloads.html')



if __name__ == '__main__':
    app.run(debug=True)
