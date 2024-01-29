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
            last_updated VARCHAR(255) NOT NULL
        )"""
    
    command3 = """CREATE TABLE weather_r(
            country VARCHAR(255) NOT NULL,
            last_updated VARCHAR(255) NOT NULL
        )"""
    
    command4 = """CREATE TABLE weather_r(
            country VARCHAR(255) NOT NULL,
            last_updated VARCHAR(255) NOT NULL
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
