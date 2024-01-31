import psycopg2



def create_tables():
    """ create tables in the PostgreSQL database"""
    
# Jeremiah's Tables
    command1 = """CREATE TABLE country (
            country VARCHAR(255) NOT NULL,
            location_name VARCHAR(255) NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timezone TIMESTAMPTZ NOT NULL
        )"""

    command2 = """CREATE TABLE weather_r(
            country VARCHAR(255) NOT NULL,
            last_updated DATE NOT NULL,
            instance_id INT NOT NULL
        )"""
    
    command3 = """CREATE TABLE wind_table(
            instance_id INT NOT NULL,
            wind_mph REAL NOT NULL,
            wind_kmh REAL NOT NULL,
            wind_degree INT NOT NULL,
            wind_direction VARCHAR(255) NOT NULL,
            gust_mph REAL NOT NULL,
            gust_kmh REAL NOT NULL
        )"""
    
    command4 = """CREATE TABLE temperature_table(
            instance_id INT NOT NULL,
            tempc REAL NOT NULL,
            tempf REAL NOT NULL,
            feelslikec REAL NOT NULL,
            feelslikef REAL NOT NULL
            
        )"""

    #Daya's Tables
    
    
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="dawsonj2",
            user="dawsonj2",
            password="eyebrow529redm")
        cur = conn.cursor()
        # create table one by one
        cur.execute(command1)
        cur.execute(command2)
        cur.execute(command3)
        cur.execute(command4)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



    
# This function tests to make sure that you can connect to the database
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

def main():
  test_connection()
  create_tables()

main()
