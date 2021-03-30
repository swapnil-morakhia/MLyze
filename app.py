import json
from os import name
from typing import Text
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from ProcessText import ProcessText
from markupsafe import escape
from flask_mongoengine import MongoEngine
import pymongo
import uuid
from functools import wraps
app = Flask(__name__)

# database
client = pymongo.MongoClient('localhost', 27017)
db = client.mydatabase

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap

def start_session(user):
    # del user['password']
    session['logged_in'] = True
    session['user'] = user
    # print(user)
    # print(session)
    return jsonify(user), 200


@app.route('/')
def home(logged_in = None):
    try: 
        logged_in = session['logged_in']
        return render_template('home.html', logged_in = logged_in)
    except:
        return render_template('home.html')

@app.route('/about')
def about(logged_in = None):
    try:
        logged_in = session['logged_in']
        return render_template('about.html', logged_in = logged_in)
    except:
        return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # print(request.form)
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        print(user)
        # user['password'] = pbkdf2_sha256.encrypt(user['password'])
        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            # return jsonify({"error": "Email address already in use"}), 400
            
            return render_template("register.html", error= "Email address already in use")

        if db.users.insert_one(user):
            # return start_session(user)
            return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login(error = None):
    
    if request.method == 'POST':
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user:
            user_password = user['password']    
            if request.form.get('password') ==  user_password:
                user_name = user['name']
                start_session(user_name)
                return redirect(url_for('dashboard', name = user_name))
            else:
                error = "Invalid credentials"
                return render_template('login.html', error = error)
        else:
            error = "Invalid credentials"
            return render_template('login.html', error = error)
    return render_template('login.html', error = error)

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard(logged_in = None):

    if request.method == 'POST':
        text = request.form['text']
        process_text = ProcessText('amazon_small.json')
        prediction = process_text.predict(text)
        return redirect(url_for('prediction', prediction=prediction))
    else:
        logged_in = session['logged_in']
        user_name = session['user']
        print(user_name)
        return render_template('dashboard.html', logged_in=logged_in)



@app.route('/<prediction>')
def prediction(prediction):
    return f'<h1>{prediction}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
