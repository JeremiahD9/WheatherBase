import psycopg2



def create_tables():
    """ create tables in the PostgreSQL database"""
    

    command1 = """CREATE TABLE cities (
            city_name VARCHAR(255) NOT NULL,
            city_state VARCHAR(255) NOT NULL,
            city_population INTEGER NOT NULL,
            city_lat REAL NOT NULL,
            city_lon REAL NOT NULL
        )"""

    command2 = """CREATE TABLE states(
            state_name VARCHAR(255) NOT NULL,
            state_abb VARCHAR(255) NOT NULL
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
