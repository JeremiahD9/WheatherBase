#!/usr/bin/python

# Imports
from flask import Flask
from flask import render_template, request, redirect, session, url_for
import psycopg2
import random
import hashlib
import os
import binascii

# Constants
PORT = 5127

# Initialize flask app
app = Flask(__name__)

# Initialize connection to the database
conn = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database = "kozakw",
    user = "kozakw",
    password = "summer862winter"
)
cur = conn.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register')
def register_page():
    return render_template("register.html")

@app.route('/user/<username>')
def home(username):
    return render_template("homepage.html", username = username)

@app.route('/submit', methods=['POST'])
def login_post():
    user_username = request.form['username']
    user_password = request.form['password']
    
    if request.method == 'POST':
        if 'login' in request.form:
            cur.execute("SELECT password,salt FROM users WHERE login='{0}';".format(user_username))
            pass_info = cur.fetchone()

            if pass_info is None:
                return render_template("login.html", incorrect_pass = True)
            else:
                correct_pass, salt = pass_info

            if hash(user_password, salt) == correct_pass:
                return redirect(url_for('home', username = user_username))
            else:
                return render_template("login.html", incorrect_pass = True)

        elif 'register' in request.form:
            cur.execute("SELECT login FROM users WHERE login='{0}';".format(user_username))
            if cur.fetchone() is not None:
                return render_template("login.html", loginText = "That username is already taken. Try again.")

            if user_username == "" or user_password == "":
                return render_template("login.html", loginText = "Please enter a username and password.")              
            salt = binascii.hexlify(os.urandom(16)).decode()
            cur.execute("INSERT INTO users VALUES ('" + user_username + "', '" + hash(user_password, salt) + "', '" + salt + "')")
            conn.commit()
            return render_template("registered.html", username = user_username)

def query_result(query):
    pass

def hash(password, salt):
    # Initialize the sha256 instance
    sha256 = hashlib.sha256()

    # Encode both the password and the salt in bytes
    b_password = password.encode()
    b_salt = salt.encode()

    # Feed both the password and salt into the hashing algorithm
    sha256.update(b_password)
    sha256.update(b_salt)

    # Return the hash
    return sha256.hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True) 