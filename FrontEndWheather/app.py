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

data_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="dawsonj2",
    user="dawsonj2",
    password="eyebrow529redm"
)
data_cur = data_conn.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/user/<username>')
def home(username):
    return render_template("homepage.html", username = username)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # If the method is POST
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user_email = request.form['email']
        user_confirm_password = request.form['confirmPassword']

        # Check if the user already exists
        cur.execute("SELECT login FROM users WHERE login='{0}';".format(user_username))
        if cur.fetchone() is not None:
            return render_template("register.html", invalid = True, error_text = "User already exists. Please try again.")

        # Check if the passwords match
        if user_password != user_confirm_password:
            return render_template("register.html", invalid = True, error_text = "Passwords do not match. Try again.")

        # Check if the username or password is blank
        if user_username == "" or user_password == "":
            return render_template("register.html", invalid = True, error_text = "Please enter a username and password.")

        # If no errors, return the template
        salt = gen_salt(16)
        cur.execute("INSERT INTO users VALUES ('{0}', '{1}', '{2}')".format(user_username, hash(user_password, salt), salt))
        conn.commit()
        return render_template("registered.html", username = user_username)

    # If the method is GET
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    # If the method is POST
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']

        # Request the password and salt from the database
        cur.execute("SELECT password,salt FROM users WHERE login='{0}';".format(user_username))
        pass_info = cur.fetchone()

        # Check to see if the user exists in the database
        if pass_info is None:
            return render_template("login.html", incorrect_pass = True)
        correct_pass, salt = pass_info

        # Check to see if the user entered password matches the database entry
        if hash(user_password, salt) == correct_pass:
            return redirect(url_for('home', username = user_username))
        return render_template("login.html", incorrect_pass = True)

    # If the method is POST
    return render_template("login.html")

# Request a query from the postgres database
def query_result(query):
    pass

# Generate a random salt
def gen_salt(size):
    return binascii.hexlify(os.urandom(size)).decode()

# Hash the password and the salt
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