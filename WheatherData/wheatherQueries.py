# This code was written by Noah and Warren

import psycopg2

def test_connection():

    conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="dawsonj2",
    user="dawsonj2",
    password="eyebrow529redm")

    if conn is not None:
        print( "Connection Worked!" )
    else:
        print( "Problem with Connection" )

    return None

def get_everything_from(table): #Works well - tested with all tables and no errors found with the tables - Noah
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT * FROM """+table+""";
        """
        
        cur.execute(sql)
        rows = cur.fetchall()

        if(rows is not None):
            for row in rows:
                print(row)
        else:
            print("No instance found")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_country_temps(country): #by Noah - Works well!
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT temperature_table.tempc, weather_r.last_updated 
        FROM temperature_table 
        JOIN weather_r ON temperature_table.instance_id = weather_r.instance_id 
        JOIN country ON weather_r.country = country.country 
        WHERE country.country = %s;
        """
        
        cur.execute(sql, (country,))
        rows = cur.fetchall()

        if(rows is not None):
            for row in rows:
                print(row)
        else:
            print("No instance found for ", country)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_highest_temp(country): #by Noah 
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT temperature_table.tempc, weather_r.last_updated 
        FROM temperature_table 
        JOIN weather_r ON temperature_table.instance_id = weather_r.instance_id 
        JOIN country ON weather_r.country = country.country
        WHERE country.country = %s
        ORDER BY temperature_table.tempc ASC 
        LIMIT 1;
        """
        
        cur.execute(sql, (country,))
        rows = cur.fetchall()

        if(rows is not None):
            for row in rows:
                print(row)
        else:
            print("No instance found for ", country)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    

def main():
    test_connection()
    get_highest_temp("China")



main()
