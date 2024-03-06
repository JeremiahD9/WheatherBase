import psycopg2

def create_tables():
    """ create tables in the PostgreSQL database"""
    
# Jeremiah's Tables
    command1 = """CREATE TABLE complete_table(
	        instance_id INT NOT NULL,
            country VARCHAR(255) NOT NULL,
            location_name VARCHAR(255) NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timezone VARCHAR(255) NOT NULL,
	        last_updated DATE NOT NULL,
            tempc REAL NOT NULL,
            tempf REAL NOT NULL,
            feelslikec REAL NOT NULL,
            feelslikef REAL NOT NULL,
	        pressure_mb REAL NOT NULL,
            pressure_in REAL NOT NULL,
            precip_mm REAL NOT NULL,
            precip_in REAL NOT NULL,
            humidity INT NOT NULL,
            cloud INT NOT NULL,
            visibility_km REAL NOT NULL,
            visibility_miles REAL NOT NULL,
            uv_index REAL NOT NULL,
            condition_text TEXT NOT NULL,
	        co REAL NOT NULL,
            ozone REAL NOT NULL,
            no2 REAL NOT NULL,
            so2 REAL NOT NULL,
            pm25 REAL NOT NULL,
            pm10 REAL NOT NULL,
            epa INT NOT NULL,
            defra INT NOT NULL,
	        sunrise TIMESTAMP NOT NULL,
            sunset TIMESTAMP NOT NULL,
            moonrise TIMESTAMP NOT NULL,
            moonset TIMESTAMP NOT NULL,
            moon_phase TEXT NOT NULL,
            moon_illumination INT NOT NULL
        )"""


    
    
    
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
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

create_tables()