#!/usr/bin/python

'''
THIS IS THE PYTHON FILE THAT WILL BE RAN TO RUN THE WEBSITE. TYPE PYTHON3 APP.PY IN THE STEARNS SERVER TO RUN THIS WEBSITE AND USE
http://stearns.mathcs.carleton.edu:5127/ TO GO TO THE MAIN PAGE.
THIS IS WHERE ALL THE PYTHON FUNCTIONS TO GO FROM PAGE TO PAGE OR COLLECT DATA FROM THE DATABASE IS HELD.

'''

# Imports
from datetime import date, time, datetime
from re import U
from flask import Flask, jsonify
from flask import render_template, request, redirect, session, url_for, send_from_directory, current_app as app
import psycopg2
import random
import hashlib
import os
import binascii
import json
import sys
import hashlib

# Constants
PORT = 5432
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
    elif pagename == 'profile':
        return render_template('profile.html', username = username, profile = "active")
    elif pagename == 'about':
        return render_template('about.html', username = username, about = "active")
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

# Sign user out
@app.route('/logout')
def logout():
    return redirect("/")

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
        SELECT DISTINCT country FROM country
        WHERE LOWER(country) LIKE %s;
        """
        
        cur.execute(sql, ( user_input + '%',))
        rows = cur.fetchall()
        cur.close()
        countryNames = [row[0] for row in rows]
        return jsonify(countryNames)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

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
            temp.tempc, 
            wind.wind_kmh, 
            prec.precip_mm, 
            sun.sunrise, 
            sun.sunset, 
            sun.moon_phase
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
        
        cur.execute(sql, (countryName, selectedDate))
        data = cur.fetchone()
        cur.close()

        sunrise_time = data[3]
        sunset_time = data[4]

        if(data):
            result = {
                'temp':data[0],
                'wind':data[1],
                'precip':data[2],
                'sunrise':sunrise_time.strftime('%I:%M %p'),
                'sunset':sunset_time.strftime('%I:%M %p'),
                'moonphase':data[5]}
            return jsonify(result)
        else:
            return jsonify({'error':'country not found'})

    except (Exception, psycopg2.DatabaseError) as error:
        app.logger.error(f"Database error: {error}")
        return jsonify({'error': str(error)}), 500
    finally:
        if conn:
            conn.close()

#HORROSCOPE STUFF - NOAH - FROM HORROSCOPE.HTML travels to HORROSCOPE-RESULTS.HTML
@app.route('/user/<username>/calculate-horoscope', methods=['GET'])
def calculate_horoscope(username):
    # Get the data from the form
    birthdate = request.args.get('birthdate')
    birthplace = request.args.get('birthplace')

    moonPhases = ["Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent", "New Moon", "New Moon"]
    sunSets = ["18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:15", "20:30", "21:00"]
    temps = ["23°C", "24°C", "25°C", "26°C", "27°C", "28°C", "29°C", "30°C", "31°C"]
    horoscopes = ["ugly loser", "beautiful soul", "ambitious achiever", "kind-hearted", "mysterious wanderer", "creative mind", "logical thinker", "empathetic listener", "dumb as a rock"]
    
    hasher = hashlib.sha256()
    hasher.update(birthdate.encode('utf-8'))
    hasher.update(birthplace.encode('utf-8'))
    hash_digest = hasher.digest()

    moon_phase_index = hash_digest[0] % len(moonPhases)
    sunset_index = hash_digest[1] % len(sunSets)
    temperature_index = hash_digest[2] % len(temps)
    horoscope_index = hash_digest[3] % len(horoscopes)

    # TEMP
    return render_template('horoscope-results.html', 
                           username=username,
                           birthdate=birthdate, 
                           birthplace=birthplace,
                           moon_phase=moonPhases[moon_phase_index],
                           sunset=sunSets[sunset_index],            
                           temperature=temps[temperature_index],
                           horoscope_final=horoscopes[horoscope_index],
                           horoscope = "active")           


# TABLE STUFF - DAYA AND JEREMIAH
@app.route('/use-date-to-get-data', methods=['GET']) 
def set_data_with_date():

    selectedDate = request.args.get('date', None)
    print(selectedDate + "In Python", file=sys.stderr)

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
            SELECT DISTINCT 
                c.country,
                c.location_name,
                c.latitude,
                c.longitude,
                c.timezone,
                w.last_updated,
                wind.wind_mph,
                wind.wind_degree,
                wind.wind_direction,
                wind.gust_mph,
                temp.tempf,
                temp.feelslikef,
                pres.pressure_in,
                pres.precip_in,
                pres.humidity,
                pres.cloud,
                pres.visibility_miles,
                pres.uv_index,
                pres.condition_text,
                air.co,
                air.ozone,
                air.no2,
                air.so2,
                air.pm25,
                air.pm10,
                air.epa,
                air.defra,
                sun.sunrise,
                sun.sunset,
                sun.moonrise,
                sun.moonset,
                sun.moon_phase,
                sun.moon_illumination
            FROM 
                country c
            INNER JOIN 
                weather_r w ON c.country = w.country
            INNER JOIN 
                wind_table wind ON w.instance_id = wind.instance_id
            INNER JOIN 
                temperature_table temp ON w.instance_id = temp.instance_id
            INNER JOIN 
                pressure_others pres ON w.instance_id = pres.instance_id
            INNER JOIN 
                airqual air ON w.instance_id = air.instance_id
            INNER JOIN 
                sunmoon sun ON w.instance_id = sun.instance_id
            WHERE 
                w.last_updated = %s;
        """
        cur.execute(sql, (selectedDate,))
        rows = cur.fetchall()  # Fetch all rows
        cur.close()

        print(len(rows), file=sys.stderr)

        results = []
        for row in rows:

            sunrise_time = row[27]
            sunset_time = row[28]
            moonrise_time = row[29]
            moonset_time = row[30]

            single_result = {
                'country': str(row[0]),
                'location_name': str(row[1]),
                'lat': str(row[2]),
                'lon': str(row[3]),
                'timezone': str(row[4]),
                'last_updated': row[5].strftime('%Y-%m-%d'),
                'wind_mph': str(row[6]),
                'wind_degree': str(row[7]),
                'wind_direction': str(row[8]),
                'gust_mph': str(row[9]),
                'tempF': str(row[10]),
                'feels_like': str(row[11]),
                'pressure_in': str(row[12]),
                'precip_in': str(row[13]),
                'humidity': str(row[14]),
                'cloud': str(row[15]),
                'visibility_miles': str(row[16]),
                'uv_index': str(row[17]),
                'condition': str(row[18]),
                'co': str(row[19]),
                'ozone': str(row[20]),
                'no2': str(row[21]),
                'so2': str(row[22]),
                'pm25': str(row[23]),
                'pm10': str(row[24]),
                'epa': str(row[25]),
                'defra': str(row[26]),
                'sunrise': sunrise_time.strftime('%I:%M %p'),  
                'sunset': sunset_time.strftime('%I:%M %p'), 
                'moonrise': moonrise_time.strftime('%I:%M %p'), 
                'moonset': moonset_time.strftime('%I:%M %p'), 
                'moonphase': str(row[31]),
                'moon_illumination': str(row[32])
            }
            results.append(single_result)

        if results:
            return jsonify(results)
        else:
            return jsonify({'error':'No data found for the given date'})

    except (Exception, psycopg2.DatabaseError) as error:
        app.logger.error(f"Database error: {error}")
        return jsonify({'error': str(error)}), 500
    finally:
        if conn:
            conn.close()



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
