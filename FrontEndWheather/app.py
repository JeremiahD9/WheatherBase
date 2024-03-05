#!/usr/bin/python

# Imports
from flask import Flask, jsonify
from flask import render_template, request, redirect, session, url_for, send_from_directory
import psycopg2
import random
import hashlib
import os
import binascii

# Constants
PORT = 5127
DEBUG = True

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

# Initialize connection to the database with the weather data
data_conn = psycopg2.connect(
    host = "localhost",
    port = 5432,
    database = "dawsonj2",
    user = "dawsonj2",
    password = "eyebrow529redm"
)
data_cur = data_conn.cursor()

# Redirect user to the login page
@app.route('/')
def index():
    return redirect('/login')

# Return each page when user is logged in
@app.route('/user/<username>/<pagename>.html')
def get_page(username, pagename):
    if pagename == 'home':
        return render_template('homepage.html', username = username, home = "active")
    elif pagename == 'map':
        return render_template('map.html', username = username, map = "active")
    elif pagename == 'table':
        return render_template('table.html', username = username, table = "active")
    elif pagename == 'horoscope':
        return render_template('horoscope.html', username = username, horoscope = "active")
    else:
        return "404"

# Register a new user
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

# Allow user to sign in
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
            return redirect(url_for('get_page', username = user_username, pagename = "home"))
        return render_template("login.html", incorrect_pass = True)

    # If the method is GET
    return render_template("login.html")

# USED IN searchbar_scripts in map.html - Noah
@app.route('/search-countries', methods=['GET']) 
def search_countries():
    user_input = request.args.get('search').lower()
    # QUERY
    #conn = None
    try:
    #    conn = psycopg2.connect(
    #    host="localhost",
    #    port=5432,
    #    database="dawsonj2",
    #   user="dawsonj2",
    #    password="eyebrow529redm")

    #    cur = conn.cursor()

        sql = """
        SELECT DISTINCT country FROM country
        WHERE LOWER(country) LIKE %s;
        """
        
        data_cur.execute(sql, ( user_input + '%',))
        rows = data_cur.fetchall()
        #cur.close()
        countryNames = [row[0] for row in rows]
        return jsonify(countryNames)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    #finally:
    #    if conn is not None:
    #        conn.close()

@app.route('/update-country', methods=['GET']) 
def update_country():
    countryName = request.args.get('country', None)
    # QUERY
    conn = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT latitude,longitude FROM country
        WHERE country = %s;
        """
        
        cur.execute(sql, ( countryName,))
        coords = cur.fetchone()
        cur.close()

        if(coords):
            return jsonify({'lat':coords[0], 'lon':coords[1]})
        else:
            return jsonify({'error':'country not found'})

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#USED IN calendarScripts.js from map.html
@app.route('/get-map-data', methods=['GET']) 
def get_map_data():
    countryName = request.args.get('country', None)
    selectedDate = request.args.get('date', None)
    # QUERY
    conn = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT 
            temp.tempc AS temperature_celsius, 
            wind.wind_kmh AS wind_kph, 
            prec.precip_mm AS precipitation_mm, 
            sun.sunrise AS sunrise, 
            sun.sunset AS sunset, 
            sun.moon_phase AS moon_phase
        FROM 
            weather_r AS wr
            INNER JOIN country AS c ON wr.country = c.country
            INNER JOIN temperature_table AS temp ON wr.instance_id = temp.instance_id
            INNER JOIN wind_table AS wind ON wr.instance_id = wind.instance_id
            INNER JOIN pressure_others AS prec ON wr.instance_id = prec.instance_id
            INNER JOIN sunmoon AS sun ON wr.instance_id = sun.instance_id
        WHERE 
            wr.country = %s AND 
            wr.last_updated = %s;
        """
        
        cur.execute(sql, ( countryName, selectedDate))
        data = cur.fetchone()
        cur.close()

        if(data):
            result = {column: value for column, value in data.items()}
            return jsonify(result)
        else:
            return jsonify({'error':'country not found'})

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# TABLE STUFF - DAYA AND JEREMIAH
@app.route('/init-table', methods=['GET']) 
def initialize_table():
    return None

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
    app.run(host = '0.0.0.0', port = PORT, debug = DEBUG)